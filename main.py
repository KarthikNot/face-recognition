import cv2
import face_recognition
import numpy as np
import json
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import threading

# Load or create face databases
saved_faces_db = "saved_faces.json"
ignored_faces_db = "ignored_faces.json"

if os.path.exists(saved_faces_db):
    with open(saved_faces_db, "r") as f:
        saved_faces = json.load(f)
else:
    saved_faces = []

if os.path.exists(ignored_faces_db):
    with open(ignored_faces_db, "r") as f:
        ignored_faces = json.load(f)
else:
    ignored_faces = []

shown_faces = set()  # Keep track of already shown faces
popup_open = False  # Flag to prevent multiple popups

def show_face_and_ask(frame, face_encoding, face_location):
    global popup_open
    if popup_open:
        return
    popup_open = True

    encoding_tuple = tuple(face_encoding)
    if encoding_tuple in shown_faces:
        popup_open = False
        return
    shown_faces.add(encoding_tuple)

    top, right, bottom, left = face_location
    frame_with_box = frame.copy()
    cv2.rectangle(frame_with_box, (left, top), (right, bottom), (0, 255, 0), 2)

    popup = tk.Toplevel()
    popup.title("Save Face")
    popup.geometry("400x500")
    popup.configure(bg="#2C3E50")

    cv2image = cv2.cvtColor(frame_with_box, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    img = img.resize((300, 300), Image.LANCZOS)
    imgtk = ImageTk.PhotoImage(image=img)

    label = tk.Label(popup, image=imgtk, bg="#2C3E50")
    label.image = imgtk
    label.pack(pady=10)

    def save_face():
        name = simpledialog.askstring("Face Recognition", "Enter name for new face:", parent=popup)
        if name:
            saved_faces.append({"name": name, "encoding": face_encoding.tolist()})
            with open(saved_faces_db, "w") as f:
                json.dump(saved_faces, f)
        close_popup()
    
    def ignore_face():
        ignored_faces.append(face_encoding.tolist())
        with open(ignored_faces_db, "w") as f:
            json.dump(ignored_faces, f)
        close_popup()
    
    def close_popup():
        global popup_open
        popup_open = False
        popup.destroy()

    tk.Button(popup, text="Save", command=save_face, bg="#27AE60", fg="white", font=("Arial", 12)).pack(pady=5)
    tk.Button(popup, text="Ignore", command=ignore_face, bg="#E74C3C", fg="white", font=("Arial", 12)).pack(pady=5)
    tk.Button(popup, text="Cancel", command=close_popup, bg="#BDC3C7", fg="black", font=("Arial", 12)).pack(pady=5)

detection_running = False
def start_detection():
    global detection_running
    if detection_running:
        return
    detection_running = True

    def detect_faces():
        global detection_running
        cap = cv2.VideoCapture(0)
        while detection_running:
            ret, frame = cap.read()
            if not ret:
                break

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding, face_location in zip(face_encodings, face_locations):
                if any(face_recognition.compare_faces([np.array(ignored)], face_encoding, tolerance=0.5)[0] for ignored in ignored_faces):
                    continue

                name = "Unknown"
                is_known = False

                for face in saved_faces:
                    if face_recognition.compare_faces([np.array(face["encoding"])], face_encoding, tolerance=0.5)[0]:
                        name = face["name"]
                        is_known = True
                        break

                if not is_known:
                    show_face_and_ask(frame, face_encoding, face_location)
                else:
                    top, right, bottom, left = face_location
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        detection_running = False

    threading.Thread(target=detect_faces, daemon=True).start()

def stop_detection():
    global detection_running
    detection_running = False

def exit_app():
    stop_detection()
    root.quit()
    root.destroy()

root = tk.Tk()
root.title("Face Recognition")
root.geometry("400x300")
root.configure(bg="#34495E")

tk.Label(root, text="Face Recognition System", font=("Arial", 16, "bold"), bg="#34495E", fg="white").pack(pady=20)
tk.Button(root, text="Start Detection", command=start_detection, bg="#27AE60", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Stop Detection", command=stop_detection, bg="#F39C12", fg="white", font=("Arial", 12)).pack(pady=10)
tk.Button(root, text="Exit", command=exit_app, bg="#E74C3C", fg="white", font=("Arial", 12)).pack(pady=10)

root.mainloop()