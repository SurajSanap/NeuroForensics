import cv2
from flask import Response
from models.face_detection import detect_criminal

def generate_frames():
    camera = cv2.VideoCapture(0)  # Open webcam

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Save frame as a temporary image for detection
        temp_image_path = "uploads/temp_frame.jpg"
        cv2.imwrite(temp_image_path, frame)

        # Detect criminal in the frame
        result = detect_criminal(temp_image_path)

        # Display detection result on the frame
        cv2.putText(frame, result, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
