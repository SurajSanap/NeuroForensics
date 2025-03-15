import cv2
import time
from ultralytics import YOLO

# Load YOLO model for weapon detection
model = YOLO("yolov8n.pt")  # Use pre-trained YOLO model

def detect_weapons(camera_id, camera_url):
    print(f"🔍 Attempting to open camera: {camera_url}")

    # Force OpenCV to use the correct backend
    cap = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)

    retries = 5
    while not cap.isOpened() and retries > 0:
        print(f"⚠️ WARNING: Retrying to connect to {camera_url} ({5 - retries}/5)")
        time.sleep(2)
        cap = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)
        retries -= 1

    if not cap.isOpened():
        print(f"❌ ERROR: Could not open camera {camera_url} after retries.")
        return

    print(f"✅ Camera {camera_url} opened successfully")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ WARNING: No frame received from camera {camera_url}")
            time.sleep(1)
            continue  # Retry reading frames

        # Run YOLO detection
        results = model(frame)
        
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2, conf, cls = box.xyxy[0].tolist()
                class_name = result.names[int(cls)]

                if class_name in ["gun", "knife"]:  # Detect weapons
                    # Draw bounding box
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)
                    cv2.putText(frame, f"{class_name} {conf:.2f}", (int(x1), int(y1) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Encode frame for video streaming
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()
