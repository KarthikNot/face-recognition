from flask import Flask, render_template, Response, jsonify, request
import cv2
import face_recognition
import numpy as np
import pymongo
import threading
import base64, os
from dotenv import load_dotenv

# Initialize Flask App
app = Flask(__name__)

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["face_recognition"]
saved_faces_db = db["saved_faces"]
ignored_faces_db = db["ignored_faces"]

# Initialize webcam
camera = cv2.VideoCapture(0)
lock = threading.Lock()
face_detected = None

# Load saved faces into memory
def load_saved_faces():
    saved_faces = list(saved_faces_db.find({}, {"_id": 0, "name": 1, "face_encoding": 1}))
    known_face_encodings = [np.array(face["face_encoding"]) for face in saved_faces]
    known_face_names = [face["name"] for face in saved_faces]
    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_saved_faces()

# Face detection function
def generate_frames():
    global face_detected
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            with lock:
                face_detected = None
                for face_encoding, (top, right, bottom, left) in zip(face_encodings, face_locations):
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
                    name = "Unknown"

                    if True in matches:
                        match_index = matches.index(True)
                        name = known_face_names[match_index]

                    else:
                        face_detected = (frame.copy(), face_encoding, (top, right, bottom, left))

                    # Draw bounding box
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    # Label the face
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save_face', methods=['POST'])
def save_face():
    global face_detected
    data = request.json
    name = data.get("name")

    with lock:
        if face_detected and name:
            frame, face_encoding, (top, right, bottom, left) = face_detected

            # Extract the face region
            face_img = frame[top:bottom, left:right]

            # Convert to Base64 for frontend display
            _, buffer = cv2.imencode('.jpg', face_img)
            face_img_base64 = base64.b64encode(buffer).decode("utf-8")

            saved_faces_db.insert_one({"name": name, "face_encoding": face_encoding.tolist(), "face_img": face_img_base64})

            # Update in-memory database
            global known_face_encodings, known_face_names
            known_face_encodings.append(np.array(face_encoding))
            known_face_names.append(name)

            face_detected = None
            return jsonify({"message": f"Face saved as {name}!"})
    
    return jsonify({"message": "No face detected or name missing!"})

@app.route('/get_saved_faces', methods=['GET'])
def get_saved_faces():
    saved_faces = list(saved_faces_db.find({}, {"_id": 0, "name": 1, "face_img": 1}))
    return jsonify(saved_faces)

@app.route('/ignore_face', methods=['POST'])
def ignore_face():
    global face_detected
    with lock:
        if face_detected:
            _, face_encoding, _ = face_detected
            ignored_faces_db.insert_one({"face_encoding": face_encoding.tolist()})
            face_detected = None
            return jsonify({"message": "Face ignored!"})
    return jsonify({"message": "No face detected!"})

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global camera
    camera.release()
    return jsonify({"message": "Face detection stopped!"})

if __name__ == "__main__":
    app.run(debug=True)
