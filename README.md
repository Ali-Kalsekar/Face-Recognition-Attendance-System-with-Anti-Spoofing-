# Face Recognition Attendance System with Anti-Spoofing
> Last automated login update: 2026-04-14 12:43:05

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.x-EE4C2C?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Real-time face recognition attendance system with anti-spoofing and SQLite logging. Built for practical deployment with modular architecture, registration flows, reporting scripts, and webcam/video support.

## Highlights

- Real-time face detection and recognition (multi-face supported)
- Anti-spoofing with liveness checks (blink/motion)
- Automatic attendance marking with duplicate-entry prevention
- SQLite persistence with exportable CSV reports
- Clean modular Python structure for scaling and maintenance

Complete production-ready Face Recognition Attendance System with anti-spoofing capabilities using OpenCV and Deep Learning. The system detects faces, recognizes registered users, prevents spoofing attacks, and stores attendance records automatically in a database.

## ÃƒÂ°Ã…Â¸Ã…Â½Ã‚Â¯ Features

### Core Features
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ **Real-Time Face Detection** - Detects faces using Haar Cascade or DNN models
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ **Face Recognition** - Identifies registered users with confidence scores
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ **Anti-Spoofing/Liveness Detection** - Prevents photo/video spoofing attacks
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ **Automatic Attendance** - Marks attendance automatically in database
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ **Duplicate Prevention** - Prevents duplicate entries within configured time window
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ **Real-Time FPS** - Shows FPS counter for performance monitoring

### Advanced Features
- ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â **Blink Detection** - Detects eye blinking for liveness
- ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â± **Motion Detection** - Detects facial motion as liveness indicator
- ÃƒÂ°Ã…Â¸Ã¢â‚¬ËœÃ‚Â¥ **Multi-Face Recognition** - Handles multiple faces in frame
- ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã…Â  **Attendance Reports** - Generate CSV reports and statistics
- ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â§ **User Registration** - Interactive registration of new users
- ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â **SQLite Database** - Persistent attendance storage
- ÃƒÂ°Ã…Â¸Ã…Â½Ã‚Â¯ **Confidence Scoring** - Shows recognition confidence
- ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã¢â‚¬Â¹ **System Logging** - Comprehensive logging system

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã¢â‚¬Â¹ Requirements

### System Requirements
- Python 3.8+
- Webcam or video source
- 4GB RAM minimum
- GPU (optional, for faster processing)

### Libraries Used
- `opencv-python` - Computer vision framework
- `face-recognition` - Face recognition library
- `dlib` - Machine learning library
- `numpy` - Numerical computing
- `pandas` - Data analysis
- `torch` - Deep learning framework
- `mediapipe` - Face detection and landmarks
- `pyyaml` - Configuration management

## ÃƒÂ°Ã…Â¸Ã…Â¡Ã¢â€šÂ¬ Installation

### Step 1: Clone/Download the Project
```bash
cd face_attendance_system
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create Necessary Directories
```bash
# Directories are created automatically, but ensure these exist:
mkdir -p dataset/known_faces
mkdir -p models
mkdir -p database
mkdir -p output
```

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã¢â‚¬â€œ Usage Guide

### Quick Start - Run the System
```bash
python main.py
```

### Register a New User
#### Method 1: Interactive Registration (During Execution)
```bash
python main.py
# Then press 'r' to enter registration mode
```

#### Method 2: Dedicated Registration Script
```bash
python register.py "Person Name"
python register.py "Person Name" --samples 10 --camera 0
```

**Registration Controls:**
- **SPACE** - Capture face sample
- **'q'** - Quit registration
- **'f'** - Finish early

### View Attendance Reports
```bash
# Today's attendance
python report.py --today

# Last 7 days
python report.py --range 7

# Specific person
python report.py --person "Person Name"

# Export to CSV
python report.py --export

# Show statistics
python report.py --stats
```

### Main Application Controls
- **'q'** - Quit application
- **'r'** - Register new user
- **SPACE** - Capture during registration

## ÃƒÂ¢Ã…Â¡Ã¢â€žÂ¢ÃƒÂ¯Ã‚Â¸Ã‚Â Configuration

Edit `config/config.yaml` to customize:

```yaml
# Camera Settings
camera:
  index: 0              # Webcam index
  width: 640            # Frame width
  height: 480           # Frame height
  fps: 30               # Target FPS

# Face Detection
face_detection:
  model: "haarcascade"  # "haarcascade" or "dnn"
  confidence_threshold: 0.5

# Face Recognition
face_recognition:
  model: "hog"          # "hog" (fast) or "cnn" (accurate)
  confidence_threshold: 0.6
  distance_threshold: 0.6

# Liveness Detection
liveness_detection:
  method: "blink_motion"  # Detection method
  blink_threshold: 0.2
  motion_threshold: 5.0

# Database
database:
  path: "./database/attendance.db"
  duplicate_prevention_minutes: 1440  # 24 hours
```

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã¢â‚¬Å¡ Project Structure

```
face_attendance_system/
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ main.py                          # Main application
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ register.py                      # User registration script
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ report.py                        # Report generation script
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ requirements.txt                 # Python dependencies
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ face_detection/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ __init__.py
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ face_detector.py            # Face detection module
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ face_recognition/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ __init__.py
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ recognizer.py               # Face recognition module
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ liveness_detection/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ __init__.py
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ anti_spoof.py              # Liveness/anti-spoofing module
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ database/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ __init__.py
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ attendance.db              # SQLite database (auto-created)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ attendance_db.py           # Database management
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ utils/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ __init__.py
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ logger.py                  # Logging utility
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ fps.py                     # FPS counter
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ draw.py                    # Drawing utilities
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ dataset/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ known_faces/               # Registered faces storage
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ models/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ (Pre-trained models)
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ config/
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ config.yaml                # Configuration file
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ output/
    ÃƒÂ¢Ã¢â‚¬ÂÃ…â€œÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ attendance_log.csv         # Exported attendance
    ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ system.log                 # System logs
```

## ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â§ System Architecture

### Components

1. **FaceDetector** - Detects faces using Haar Cascade or DNN
2. **FaceRecognizer** - Recognizes faces from registered dataset
3. **AntiSpoofDetector** - Detects liveness using motion/blink
4. **AttendanceDatabase** - Manages SQLite database
5. **Utils** - FPS counter, drawing, and logging

### Data Flow
```
Video Input
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Face Detection
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Face Recognition
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Liveness Detection
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Mark Attendance (if real + recognized)
    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬Å“
Visualization & Storage
```

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã…Â  Database Schema

### attendance Table
```sql
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    timestamp DATETIME,
    status TEXT DEFAULT 'Present',
    confidence REAL,
    liveness_status TEXT DEFAULT 'REAL',
    date TEXT,
    time TEXT
);
```

### users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE,
    registration_time DATETIME,
    status TEXT DEFAULT 'Active'
);
```

## ÃƒÂ°Ã…Â¸Ã…Â½Ã‚Â¨ Visualization

The system displays:
- **Face Bounding Box** - Green box around detected face
- **Person Name** - Recognized person's name
- **Confidence Score** - Recognition confidence (0-1)
- **Liveness Status** - "REAL" or "FAKE"
- **FPS Counter** - Real-time FPS

```
ÃƒÂ¢Ã¢â‚¬ÂÃ…â€™ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‚Â
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡    Ali             ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  Conf: 0.95        ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡  Status: REAL      ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡ FPS: 25.5
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡                   ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬Å¡
ÃƒÂ¢Ã¢â‚¬ÂÃ¢â‚¬ÂÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ¢â€šÂ¬ÃƒÂ¢Ã¢â‚¬ÂÃ‹Å“
```

## ÃƒÂ°Ã…Â¸Ã…Â¡Ã¢â€šÂ¬ Performance Optimization

### GPU Support
To use GPU acceleration (if available):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Model Selection
- **HOG Model** - Faster, suitable for real-time (default)
- **CNN Model** - More accurate but slower

Change in config:
```yaml
face_recognition:
  model: "cnn"  # For accuracy over speed
```

## ÃƒÂ°Ã…Â¸Ã‚ÂÃ¢â‚¬Âº Troubleshooting

### Camera Not Opening
```bash
# Check available cameras
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```

### Face Not Detected
- Improve lighting conditions
- Move closer to camera
- Adjust face_detection configuration

### Recognition Issues
- Register with more samples (10-20)
- Ensure clear, frontal face images
- Reduce distance_threshold in config if needed

### Performance Issues
- Reduce frame resolution
- Use HOG model instead of CNN
- Update graphics drivers

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‚Â Example Usage

### Complete Workflow

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Register users
python register.py "Alice" --samples 10
python register.py "Bob" --samples 10

# 3. Run attendance system
python main.py

# 4. View reports
python report.py --today

# 5. Export attendance
python report.py --export
```

## ÃƒÂ°Ã…Â¸Ã…Â½Ã¢â‚¬Å“ Training & Customization

### Adding More Face Samples
```bash
python register.py "Person Name" --samples 20
```

### Adjusting Detection Sensitivity
Edit `config/config.yaml`:
```yaml
face_detection:
  confidence_threshold: 0.7  # Increase for stricter
```

### Adjusting Recognition Threshold
```yaml
face_recognition:
  distance_threshold: 0.5    # Lower = stricter
```

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã‹â€  Scalability

The system supports:
- Multi-camera setups (modify config)
- Multiple users (unlimited)
- Long-term database (auto-archives old records)
- Distributed processing (with modifications)

## ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â Security Features

1. **Anti-Spoofing** - Prevents photo/video attacks
2. **Liveness Detection** - Ensures real face
3. **Duplicate Prevention** - One entry per person per day
4. **Confidence Threshold** - Rejects low-confidence matches
5. **Logging** - Full audit trail

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã…Â¾ Support & Troubleshooting

### Check System Status
```bash
python -c "from main import FaceAttendanceSystem; s = FaceAttendanceSystem(); print(s.recognizer.get_statistics())"
```

### View Logs
```bash
# Latest log file is in output/
cat output/system_DD_MM_YYYY.log
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Camera not found | Check camera index in config.yaml |
| Face not detected | Improve lighting, move closer |
| Unknown person | Register with more samples |
| Slow performance | Use HOG model, reduce resolution |
| Database locked | Restart application |

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã¢â‚¬Å¾ License

This system is provided as-is for educational and commercial use.

## ÃƒÂ°Ã…Â¸Ã‚Â¤Ã‚Â Contributing

Improvements and suggestions welcome!

## ÃƒÂ°Ã…Â¸Ã¢â‚¬Å“Ã…Â¡ References

- [OpenCV Documentation](https://docs.opencv.org/)
- [face_recognition Library](https://github.com/ageitgey/face_recognition)
- [MediaPipe Face Detection](https://google.github.io/mediapipe/)
- [dlib Documentation](http://dlib.net/)

---

**Built with ÃƒÂ¢Ã‚ÂÃ‚Â¤ÃƒÂ¯Ã‚Â¸Ã‚Â using Python, OpenCV, and Deep Learning**

For production deployment, consider:
- GPU acceleration
- Multi-threading for multiple cameras
- Cloud database integration
- Docker containerization
- REST API endpoints
