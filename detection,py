import cv2
from deepface import DeepFace

def recognize_face(image_path, criminal_image_path):
    result = DeepFace.verify(img1_path=image_path, img2_path=criminal_image_path, model_name="VGG-Face")
    return result["verified"]
