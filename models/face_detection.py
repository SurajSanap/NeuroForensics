import cv2
import os
import json
import numpy as np
from datetime import datetime
from deepface import DeepFace
from models.database import Criminal

# Load OpenCV face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

def detect_faces_and_save(frame, save_path):
    """
    Detects faces, draws bounding boxes, and saves detected faces with timestamps.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    detected_faces = []
    for (x, y, w, h) in faces:
        face_img = frame[y:y+h, x:x+w]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{save_path}/face_{timestamp}.jpg"
        cv2.imwrite(filename, face_img)  # Save the face image
        detected_faces.append(filename)

        # Draw bounding box on the frame
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    return frame, detected_faces

def detect_criminal(image_path):
    """
    Detects whether the given image contains a face that matches any known criminals.
    """
    try:
        face_embedding = DeepFace.represent(img_path=image_path, model_name="VGG-Face")[0]["embedding"]
        criminals = Criminal.query.all()
        for criminal in criminals:
            stored_embedding = json.loads(criminal.face_encoding)
            distance = np.linalg.norm(np.array(stored_embedding) - np.array(face_embedding))

            if distance < 0.6:  # Match threshold
                return criminal  # Matched criminal

    except Exception as e:
        print(f"Error in detection: {e}")

    return None
