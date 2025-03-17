import logging
import os
from flask import Flask, render_template, request, redirect, flash, jsonify, url_for, Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from models.database import db
import cv2

# Import models
from models.database import db, User, Criminal, Camera
from models.weapon_detection import detect_weapons
from models.detection import detect_criminal

# Initialize Flask App
app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'uploads'

migrate = Migrate(app, db)
# Initialize Database
db.init_app(app)

# Flask-Login Setup
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------- Authentication Routes -------------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered!", "danger")
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials, try again.", "danger")

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

# ------------------- Main Routes -------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dashboard')
@login_required
def dashboard():
    cameras = Camera.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', cameras=cameras)


@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("No file uploaded")
            return redirect('/upload')

        file = request.files['file']
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        result = detect_criminal(filepath)
        flash(f"Detection Complete: {result}")
        return redirect('/dashboard')

    return render_template('upload.html')


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/premium')
@login_required
def premium():
    return render_template('premium.html')


@app.route('/register_camera', methods=['GET', 'POST'])
@login_required
def register_camera():
    if request.method == 'POST':
        camera_name = request.form['camera_name']
        camera_url = request.form['camera_url']
        enable_face_detection = 'face_detection' in request.form
        enable_weapon_detection = 'weapon_detection' in request.form
        
        new_camera = Camera(
            user_id=current_user.id,
            camera_name=camera_name,
            camera_url=camera_url,
            enable_face_detection=enable_face_detection,
            enable_weapon_detection=enable_weapon_detection
        )

        db.session.add(new_camera)
        db.session.commit()
        flash("Camera Registered Successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('register_camera.html')

@app.route('/manage_cameras')
@login_required
def manage_cameras():
    cameras = Camera.query.filter_by(user_id=current_user.id).all()
    return render_template('manage_cameras.html', cameras=cameras)

@app.route('/delete_camera/<int:id>')
@login_required
def delete_camera(id):
    camera = Camera.query.filter_by(id=id, user_id=current_user.id).first()

    if camera:
        db.session.delete(camera)
        db.session.commit()
        flash("Camera Deleted Successfully!", "success")
    else:
        flash("Unauthorized Action!", "danger")

    return redirect(url_for('manage_cameras'))

@app.route('/add_criminal', methods=['GET', 'POST'])
@login_required
def add_criminal():
    if request.method == 'POST':
        name = request.form['name']
        crime_details = request.form['crime_details']
        file = request.files['image']

        if not name or not crime_details or 'image' not in request.files:
            flash("All fields are required!", "danger")
            return redirect(url_for('add_criminal'))

        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        # Save criminal in the database
        new_criminal = Criminal(name=name, crime_details=crime_details, image_path=image_path, face_encoding="TBD")
        db.session.add(new_criminal)
        db.session.commit()

        flash("Criminal Added Successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_criminal.html')

@app.route('/video_feed/<int:camera_id>')
@login_required
def video_feed(camera_id):
    camera = Camera.query.filter_by(id=camera_id, user_id=current_user.id).first()
    if not camera:
        return "Camera not found!", 404
    return Response(stream_camera(camera.camera_url), mimetype='multipart/x-mixed-replace; boundary=frame')

# Function to Stream Camera
def stream_camera(camera_url):
    logging.info(f"🔍 Attempting to open camera: {camera_url}")
    
    # Ensure URL format
    if not camera_url.startswith("http") and not camera_url.startswith("rtsp"):
        camera_url = f"http://{camera_url}/video"
    
    cap = cv2.VideoCapture(camera_url, cv2.CAP_FFMPEG)  # Using OpenCV with FFMPEG backend
    
    if not cap.isOpened():
        logging.error(f"❌ ERROR: Could not open camera at {camera_url}")
        return
    
    logging.info(f"✅ Camera {camera_url} opened successfully")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            logging.warning(f"⚠️ WARNING: No frame received from {camera_url}")
            continue
        
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    
    cap.release()

@app.route('/weapon_video_feed/<int:camera_id>')
@login_required
def weapon_video_feed(camera_id):
    camera = Camera.query.filter_by(id=camera_id, user_id=current_user.id).first()
    if not camera:
        return "Camera not found!", 404
    
    logging.info(f"🎥 Starting weapon detection stream for Camera ID: {camera_id}")
    
    return Response(detect_weapons(camera.id, camera.camera_url),
                    mimetype='multipart/x-mixed-replace; boundary=frame',
                    headers={"Cache-Control": "no-cache"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
