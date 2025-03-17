

<p align="center">
  <img src="https://github.com/user-attachments/assets/246952ec-7f50-49da-a683-5cfb6d11a6b0" width="150">
</p>


# NeuroForensics: AI-Powered Criminal Detection System

## 📌 Introduction
NeuroForensics is an **AI-powered criminal detection system** that leverages **deep learning**, **OpenCV**, and **real-time surveillance** to enhance security operations. It integrates with security cameras, performs **facial recognition**, and detects **weapons** to assist law enforcement in proactive crime prevention.

## 🚀 Features
✅ **Real-time Video Processing** - Stream live camera feeds with OpenCV.  
✅ **Facial Recognition** - Identify known criminals using deep learning models (DeepFace).  
✅ **Weapon Detection** - Detect firearms and knives using AI models.  
✅ **Database Management** - Store and retrieve criminal profiles with crime details.  
✅ **Secure Authentication** - User login system to manage cameras and detections.  
✅ **Automated Alerts** - Log detections with timestamps for forensic analysis.  

## 🏗️ Technology Stack
- **Python** (Flask for the backend)
- **OpenCV** (Real-time video streaming & processing)
- **DeepFace** (Facial recognition)
- **YOLO** (Weapon detection)
- **SQLite** (Database storage)
- **HTML, CSS, JavaScript** (Frontend interface)

## Flowchart:

flowchart TD
                A[Start] --> B[User Login/Register]
                B --> C[Dashboard]
                C --> D[Manage Cameras]
                D --> E[Register Camera]
                D --> F[Delete Camera]
                C --> G[Stream Camera]
                G --> H[Face Detection]
                G --> I[Weapon Detection]
                H --> J[Store Detection Data]
                I --> J
                I --> K[Trigger Alert]
                J --> L[Generate Report]
                K --> L
                L --> M[End]

## 🔧 Installation Guide
### **Step 1: Clone the Repository**
```bash
git clone https://github.com/your-repo/NeuroForensics.git
cd NeuroForensics
```

### **Step 2: Create a Virtual Environment**
```bash
python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Setup the Database**
```bash
python
>>> from app import db
>>> db.create_all()
>>> exit()
```

### **Step 5: Run the Application**
```bash
python app.py
```
Access the web interface at: **`http://127.0.0.1:5000`**

## 📂 Project Structure
```
NeuroForensics/
│── models/
│   ├── database.py      # Database models
│   ├── face_detection.py # Face recognition logic
│   ├── weapon_detection.py # Weapon detection logic
│── templates/
│   ├── dashboard.html   # Live monitoring interface
│   ├── manage_cameras.html # Camera management UI
│── static/
│── uploads/            # Criminal images storage
│── app.py              # Main Flask application
│── requirements.txt    # Dependencies
│── README.md           # Project documentation
```

## 🎯 How It Works
1️⃣ **Register Cameras** - Add security cameras via IP streams.  
2️⃣ **Real-time Face & Weapon Detection** - Detect criminals & weapons live.  
3️⃣ **Store Criminal Data** - Save face encodings in the database.  
4️⃣ **Forensic Logging** - Capture and store images for forensic analysis.  

## 🤖 AI Models Used
- **DeepFace** for face recognition.
- **YOLO (You Only Look Once)** for object (weapon) detection.
- **OpenCV** for real-time image processing.

## 📜 License
This project is licensed under the MIT License.


## 📬 Contact
For queries, reach out via email: `surajsanapcontact@gmail.com`

**Let's build a safer world with AI-powered crime detection!**


