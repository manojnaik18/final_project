from flask import Flask, render_template, request, redirect, send_from_directory,jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['bus_database']
passengers_collection = db['passengers']
fares_collection=db['fares']

# Serve static files (like face images) from the 'faces' directory
@app.route('/faces/<filename>')
def get_face_image(filename):
    return send_from_directory('faces', filename)



# Route to fetch the available sources and destinations from the fares collection
@app.route('/get_fares', methods=['GET'])
def get_fares():
    # Convert the cursor to a list to iterate over it multiple times
    fares = list(fares_collection.find())

    # Extract sources and destinations
    sources = set(fare['source'] for fare in fares)
    destinations = set(fare['destination'] for fare in fares)
    
    # Return both sources and destinations as a JSON response
    return jsonify(list(sources), list(destinations))


# Route to fetch the amount for the selected source-destination pair
@app.route('/get_amount', methods=['POST'])
def get_amount():
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    fare = fares_collection.find_one({'source': source, 'destination': destination})
    
    if fare:
        return jsonify({'amount': fare['amount']})
    return jsonify({'amount': 0})





# Home route to list all unverified passengers
@app.route('/')
def index():
    unverified_passengers = passengers_collection.find({'verified': False})
    return render_template('index.html', passengers=unverified_passengers)

# Route to issue a ticket and verify the passenger
@app.route('/issue_ticket/<passenger_id>', methods=['POST'])
def issue_ticket(passenger_id):
    source = request.form['source']
    destination = request.form['destination']
    amount = request.form['amount']
    
    passengers_collection.update_one(
        {'_id': ObjectId(passenger_id)},
        {
            '$set': {
                'verified': True,
                'source': source,
                'destination': destination,
                'amount': float(amount)
            }
        }
    )
    
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
