"""
Advanced Features and API Documentation
Face Recognition Attendance System
"""

# ADVANCED FEATURES GUIDE

## Custom Face Recognition Model

### Using a Different Recognition Model

```python
from face_recognition import FaceRecognizer

# Use CNN model for higher accuracy
recognizer = FaceRecognizer(
    dataset_path="./dataset/known_faces",
    distance_threshold=0.55,
    model_type="cnn"  # "hog" or "cnn"
)
```

## Custom Liveness Detection

### Implement Custom Liveness Method

```python
from liveness_detection import AntiSpoofDetector

class CustomLivenessDetector(AntiSpoofDetector):
    def _custom_detection(self, frame):
        # Implement custom logic
        # Return: (is_live, confidence)
        return True, 0.8

detector = CustomLivenessDetector(method="custom")
```

## API Reference

### FaceDetector Class

```python
from face_detection import FaceDetector

# Initialize
detector = FaceDetector(
    model_type="haarcascade",  # or "dnn"
    confidence_threshold=0.5
)

# Detect faces
faces = detector.detect_faces(
    frame,
    scale_factor=1.1,
    neighbors=5
)
# Returns: [(x, y, w, h), ...]

# Get info
info = detector.get_detector_info()
```

### FaceRecognizer Class

```python
from face_recognition import FaceRecognizer

# Initialize
recognizer = FaceRecognizer(
    dataset_path="./dataset/known_faces",
    distance_threshold=0.6,
    model_type="hog"
)

# Recognize single face
name, confidence = recognizer.recognize_face(frame, face_location)

# Recognize multiple faces
results = recognizer.recognize_faces_batch(frame, face_locations)

# Add new person
added_count = recognizer.add_person("New Person", image_paths)

# Get statistics
stats = recognizer.get_statistics()
```

### AttendanceDatabase Class

```python
from database import AttendanceDatabase

# Initialize
db = AttendanceDatabase(
    db_path="./database/attendance.db",
    duplicate_prevention_minutes=1440
)

# Mark attendance
success = db.mark_attendance(
    name="John Doe",
    confidence=0.95,
    liveness_status="REAL"
)

# Get reports
df = db.get_attendance_report(date_str="25-12-2024")
df = db.get_all_attendance(days=30)

# Export
db.export_attendance_csv(output_path="./output/attendance.csv")

# User management
db.register_user("New User")
count = db.get_today_attendance_count()
```

## Integration Examples

### Flask Web Interface

```python
from flask import Flask, render_template, jsonify
from main import FaceAttendanceSystem

app = Flask(__name__)
system = FaceAttendanceSystem()

@app.route('/api/attendance/today')
def get_today_attendance():
    """Get today's attendance."""
    attendance = system.database.get_today_attendance_list()
    return jsonify({"attendance": attendance})

@app.route('/api/stats')
def get_stats():
    """Get system statistics."""
    stats = system.recognizer.get_statistics()
    return jsonify(stats)

if __name__ == "__main__":
    app.run(debug=True)
```

### Multi-Camera Setup

```python
import threading
from main import FaceAttendanceSystem

def process_camera(camera_index, camera_name):
    """Process single camera."""
    system = FaceAttendanceSystem()
    system.config['camera']['index'] = camera_index
    # Process frames from this camera
    print(f"Processing camera: {camera_name}")

# Start multiple threads
cameras = [
    (0, "Entrance"),
    (1, "Exit"),
    (2, "Office")
]

threads = []
for cam_index, cam_name in cameras:
    thread = threading.Thread(
        target=process_camera,
        args=(cam_index, cam_name)
    )
    thread.start()
    threads.append(thread)

# Wait for all threads
for thread in threads:
    thread.join()
```

### REST API Server

```python
from fastapi import FastAPI
from database import AttendanceDatabase

app = FastAPI()
db = AttendanceDatabase()

@app.get("/api/attendance/{person_name}")
async def get_person_attendance(person_name: str):
    """Get specific person's attendance."""
    df = db.get_all_attendance(days=30)
    person_data = df[df['name'] == person_name]
    return {"attendance": person_data.to_dict(orient='records')}

@app.post("/api/register/{person_name}")
async def register_person(person_name: str):
    """Register new person."""
    success = db.register_user(person_name)
    return {"success": success}

@app.get("/api/report/daily")
async def get_daily_report():
    """Get daily attendance report."""
    df = db.get_attendance_report()
    return {"report": df.to_dict(orient='records')}
```

## Performance Tuning

### Reduce Latency

```yaml
# For fastest response
face_detection:
  model: "haarcascade"
  confidence_threshold: 0.3
  scale_factor: 1.3
  neighbors: 4

face_recognition:
  model: "hog"
  distance_threshold: 0.7

# Reduce frame resolution
camera:
  width: 320
  height: 240
```

### Improve Accuracy

```yaml
# For best recognition accuracy
face_detection:
  model: "dnn"
  confidence_threshold: 0.8

face_recognition:
  model: "cnn"
  distance_threshold: 0.4

# Larger resolution
camera:
  width: 1280
  height: 960
```

## Machine Learning Customization

### Fine-tune Recognition Model

```python
import face_recognition
import numpy as np

# Train custom recognizer
known_encodings = []
known_labels = []

for person_name in os.listdir("./dataset/known_faces"):
    for image_file in os.listdir(f"./dataset/known_faces/{person_name}"):
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        
        known_encodings.extend(encodings)
        known_labels.extend([person_name] * len(encodings))

# Use for recognition
distances = face_recognition.face_distance(known_encodings, unknown_encoding)
```

## Database Queries

### Advanced SQLite Queries

```python
import sqlite3

conn = sqlite3.connect("./database/attendance.db")
cursor = conn.cursor()

# Get attendance by date
cursor.execute("""
    SELECT name, COUNT(*) as count 
    FROM attendance 
    WHERE date = ? 
    GROUP BY name
""", ("25-12-2024",))

# Get top attendees
cursor.execute("""
    SELECT name, COUNT(*) as count 
    FROM attendance 
    GROUP BY name 
    ORDER BY count DESC 
    LIMIT 10
""")

# Get daily statistics
cursor.execute("""
    SELECT date, COUNT(*) as total 
    FROM attendance 
    GROUP BY date 
    ORDER BY date DESC
""")
```

## Custom Configuration

### Load Custom Config

```python
import yaml

def load_custom_config(config_path):
    """Load custom configuration."""
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config

config = load_custom_config("./config/production.yaml")
```

### Environment Variables

```python
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.getenv("ATTENDANCE_DB_PATH", "./database/attendance.db")
camera_index = int(os.getenv("CAMERA_INDEX", "0"))
```

## Logging and Debugging

### Extended Logging

```python
from utils import get_logger
import logging

logger = get_logger()
logger.setLevel(logging.DEBUG)

# Log detailed information
logger.debug("Face detection started")
logger.info("Attendance marked")
logger.warning("Low recognition confidence")
logger.error("Camera not found")
```

## Error Handling

### Try-Catch Best Practices

```python
from face_detection import FaceDetector
from utils import get_logger

logger = get_logger()

try:
    detector = FaceDetector()
except Exception as e:
    logger.error(f"Failed to initialize detector: {e}")
    # Fallback or handle error

try:
    faces = detector.detect_faces(frame)
except Exception as e:
    logger.warning(f"Detection failed: {e}")
    faces = []
```

## Performance Monitoring

### Monitor System Performance

```python
import psutil
import time

def monitor_performance():
    """Monitor system resources."""
    
    # CPU usage
    cpu_percent = psutil.cpu_percent(interval=1)
    
    # Memory usage
    memory_info = psutil.virtual_memory()
    memory_percent = memory_info.percent
    
    # Camera FPS
    fps = fps_counter.get_fps()
    
    print(f"CPU: {cpu_percent}%")
    print(f"Memory: {memory_percent}%")
    print(f"FPS: {fps}")
    
    return {
        'cpu': cpu_percent,
        'memory': memory_percent,
        'fps': fps
    }
```

## Troubleshooting Advanced Issues

### Debug Face Detection

```python
def debug_detection(frame):
    """Debug detection issues."""
    faces = detector.detect_faces(frame)
    
    print(f"Detected {len(faces)} faces")
    
    for i, face in enumerate(faces):
        x, y, w, h = face
        print(f"Face {i}: x={x}, y={y}, w={w}, h={h}")
        
        # Draw bounding box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    cv2.imshow("Detection Debug", frame)
```

### Profile Recognition Speed

```python
import time

def profile_recognition():
    """Profile recognition performance."""
    
    start = time.time()
    name, confidence = recognizer.recognize_face(frame, face_location)
    elapsed = time.time() - start
    
    print(f"Recognition took: {elapsed*1000:.2f}ms")
    print(f"Average: {1000/elapsed:.1f} fps")
```

## Contributing and Extensions

### Create Custom Face Detector

```python
class CustomFaceDetector:
    """Custom face detection implementation."""
    
    def __init__(self):
        # Initialize custom model
        pass
    
    def detect_faces(self, frame):
        # Implement detection
        return []
```

### Add Custom Liveness Method

```python
class CustomLivenessDetector:
    """Custom liveness detection."""
    
    def detect_liveness(self, frame):
        # Implement custom logic
        # Return: (is_live, confidence, status)
        return True, 0.8, "REAL"
```

---

**For more information, see README.md and DEPLOYMENT.md**
