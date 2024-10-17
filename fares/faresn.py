from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['bus_database']
fares_collection = db['fares']

# Insert source-destination pairs with amounts
fares = [
    {"source": "Stop A", "destination": "Stop X", "amount": 50},
    {"source": "Stop A", "destination": "Stop Y", "amount": 60},
    {"source": "Stop B", "destination": "Stop X", "amount": 40},
    {"source": "Stop B", "destination": "Stop Z", "amount": 70},
    {"source": "Stop C", "destination": "Stop Y", "amount": 55},
]

# Insert into the fares collection
fares_collection.insert_many(fares)

print("Inserted source-destination fares into MongoDB.")
