import cv2
import os
import time
from pymongo import MongoClient
from bson import ObjectId

# Create necessary directories
if not os.path.exists('faces'):
    os.makedirs('faces')

# Initialize camera
cap = cv2.VideoCapture(0)

# Load OpenCV's pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')  # Update with your MongoDB connection string if needed
db = client['bus_database']  # Database name
passengers_collection = db['passengers']  # Collection name

def store_face(face_img):
    # Save image to disk (name based on timestamp)
    filename = f"faces/face_{int(time.time())}.png"
    cv2.imwrite(filename, face_img)

    # Insert record into the MongoDB collection
    passengers_collection.insert_one({
        'face_image': filename,
        'verified': False,
        'source': None,
        'destination': None,
        'amount': None
    })

# Keep track of detected faces to avoid duplication
last_face_time = time.time()

# Set the time threshold between capturing faces (e.g., 5 seconds)
capture_interval = 3

# Set the total capture duration (e.g., 15 seconds)
total_duration = 4
start_time = time.time()

# Start the video feed and automatic face capture
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # If a face is detected and enough time has passed, capture the face
    if len(faces) > 0 and time.time() - last_face_time > capture_interval:
        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]  # Extract the face area
            store_face(face)  # Store the face in the MongoDB
            
            # Update the last capture time to avoid repeated captures
            last_face_time = time.time()

    # Display the video feed (optional)
    cv2.imshow('Face Capture', frame)

    # Break the loop after 15 seconds
    if time.time() - start_time > total_duration:
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()

# Close the MongoDB connection
client.close()
