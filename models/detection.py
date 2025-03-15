import cv2
import json
import numpy as np
from deepface import DeepFace
from models.database import Criminal

def detect_criminal(image_path):
    """
    Detects whether the given image contains a face that matches any known criminals.
    """
    try:
        # Extract face embedding from the image
        face_embedding = DeepFace.represent(img_path=image_path, model_name="VGG-Face")[0]["embedding"]

        # Fetch all stored criminals
        criminals = Criminal.query.all()
        for criminal in criminals:
            stored_embedding = json.loads(criminal.face_encoding)
            distance = np.linalg.norm(np.array(stored_embedding) - np.array(face_embedding))

            if distance < 0.6:  # Threshold for face match
                return criminal  # Return the matched criminal

    except Exception as e:
        print(f"Error in detection: {e}")

    return None  # No match found
