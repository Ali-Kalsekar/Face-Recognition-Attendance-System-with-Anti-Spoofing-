"""
INSTALLATION AND QUICK REFERENCE CARD
Face Recognition Attendance System
"""

__version__ = "1.0.0"
__author__ = "Face Recognition Team"
__date__ = "2024"

# ============================================================
# INSTALLATION (COPY & PASTE THESE COMMANDS)
# ============================================================

"""
# WINDOWS
1. Open Command Prompt or PowerShell
2. Navigate to project folder:
   cd face_attendance_system

3. Create virtual environment:
   python -m venv venv

4. Activate virtual environment:
   venv\Scripts\activate

5. Install dependencies:
   pip install -r requirements.txt

6. Run setup (optional, auto-creates directories):
   python setup.py

7. Register first user:
   python register.py "Your Name"

8. Run the system:
   python main.py


# LINUX / MAC
1. Open Terminal
2. Navigate to project folder:
   cd face_attendance_system

3. Create virtual environment:
   python3 -m venv venv

4. Activate virtual environment:
   source venv/bin/activate

5. Install dependencies:
   pip install -r requirements.txt

6. Register first user:
   python3 register.py "Your Name"

7. Run the system:
   python3 main.py
"""

# ============================================================
# QUICK REFERENCE - MOST USED COMMANDS
# ============================================================

COMMANDS = {
    "Start System": "python main.py",
    "Register User": "python register.py \"Name\"",
    "View Today's Attendance": "python report.py --today",
    "View Last 7 Days": "python report.py --range 7",
    "View Person History": "python report.py --person \"Name\"",
    "Export Report": "python report.py --export",
    "Show Statistics": "python report.py --stats",
    "System Health Check": "python health_check.py",
    "Process Video": "python video_processor.py video.mp4",
    "Run Tests": "python test_system.py"
}

# ============================================================
# KEYBOARD SHORTCUTS (DURING EXECUTION)
# ============================================================

SHORTCUTS = {
    "'q'": "Quit application",
    "'r'": "Register new user (during main.py)",
    "SPACE": "Capture face sample (during registration)"
}

# ============================================================
# FILE DESCRIPTIONS
# ============================================================

FILES = {
    "main.py": "Main application - START HERE",
    "register.py": "Register new users",
    "report.py": "Generate attendance reports",
    "video_processor.py": "Process offline videos",
    "health_check.py": "System diagnostics",
    "setup.py": "Automated setup script",
    "test_system.py": "Unit tests",
    
    "config/config.yaml": "System configuration",
    "requirements.txt": "Python dependencies",
    
    "README.md": "Complete documentation (15 min read)",
    "QUICKSTART.md": "5-minute quick start guide",
    "DEPLOYMENT.md": "Production deployment guide",
    "ADVANCED.md": "API reference and advanced features",
    "PROJECT_OVERVIEW.md": "Project structure and overview"
}

# ============================================================
# COMMON CONFIGURATIONS
# ============================================================

QUICK_CONFIGS = {
    "Fast Mode (Low Latency)": {
        "face_detection_model": "haarcascade",
        "face_recognition_model": "hog",
        "camera_resolution": "320x240",
        "expected_fps": "20-30"
    },
    
    "Balanced Mode (Default)": {
        "face_detection_model": "haarcascade",
        "face_recognition_model": "hog",
        "camera_resolution": "640x480",
        "expected_fps": "15-25"
    },
    
    "Accuracy Mode (High Quality)": {
        "face_detection_model": "dnn",
        "face_recognition_model": "cnn",
        "camera_resolution": "1280x960",
        "expected_fps": "5-10",
        "note": "Slower but more accurate"
    }
}

# ============================================================
# TROUBLESHOOTING QUICK GUIDE
# ============================================================

TROUBLESHOOTING = {
    "Camera not detected": [
        "1. Check camera connection",
        "2. Try different camera index in config.yaml",
        "3. Run: python -c \"import cv2; print(cv2.VideoCapture(0).isOpened())\""
    ],
    
    "Face not detected": [
        "1. Improve lighting",
        "2. Move closer to camera",
        "3. Try different angle",
        "4. Adjust confidence_threshold in config.yaml"
    ],
    
    "Person not recognized": [
        "1. Register with more samples (15-20)",
        "2. Ensure clear, frontal face images",
        "3. Lower distance_threshold in config.yaml",
        "4. Use CNN model for better accuracy"
    ],
    
    "Slow performance": [
        "1. Reduce camera resolution",
        "2. Use HOG model instead of CNN",
        "3. Enable GPU acceleration (if available)",
        "4. Check system CPU/Memory usage"
    ],
    
    "Dependencies not installing": [
        "1. Upgrade pip: pip install --upgrade pip",
        "2. Install system dependencies (dlib, cmake)",
        "3. Try: pip install -r requirements.txt --no-cache-dir"
    ]
}

# ============================================================
# DIRECTORY STRUCTURE EXPLAINED
# ============================================================

STRUCTURE = """
face_attendance_system/
├── main.py                    ← RUN THIS TO START
├── requirements.txt           ← Install: pip install -r requirements.txt
├── config/
│   └── config.yaml           ← Adjust settings here
├── face_detection/            ← Face detection module
├── face_recognition/          ← Face recognition module
├── liveness_detection/        ← Anti-spoofing module
├── database/                  ← SQLite database
├── utils/                     ← Logging, FPS, drawing
├── dataset/
│   └── known_faces/          ← Registered faces stored here
├── output/
│   ├── attendance_log.csv    ← Reports exported here
│   └── system.log            ← System logs
└── README.md                  ← Full documentation
"""

# ============================================================
# CONFIGURATION QUICK TIPS
# ============================================================

CONFIG_TIPS = {
    "Faster Recognition": {
        "change": "face_recognition.model = 'hog'",
        "effect": "Faster but slightly less accurate"
    },
    
    "Better Accuracy": {
        "change": "face_recognition.model = 'cnn'",
        "effect": "More accurate but slower (needs GPU)"
    },
    
    "Stricter Matching": {
        "change": "face_recognition.distance_threshold = 0.4",
        "effect": "Only very similar faces recognized"
    },
    
    "Relaxed Matching": {
        "change": "face_recognition.distance_threshold = 0.8",
        "effect": "More permissive, may have false positives"
    },
    
    "Prevent Same-Day Duplicates": {
        "change": "database.duplicate_prevention_minutes = 1440",
        "effect": "Only one entry per person per 24 hours"
    }
}

# ============================================================
# MINIMUM REQUIREMENTS
# ============================================================

REQUIREMENTS = {
    "Python Version": "3.8 or higher",
    "RAM": "4 GB minimum (8 GB recommended)",
    "Disk Space": "2 GB for installation, 20 GB for logs",
    "Processor": "Modern CPU (Intel i5 or equivalent)",
    "GPU": "Optional but recommended for real-time",
    "Webcam": "Any USB webcam or built-in camera",
    "OS": "Windows 10+, Linux, or macOS"
}

# ============================================================
# EXPECTED RESULTS
# ============================================================

EXPECTED_RESULTS = """
After setup, you should see:

1. Main Window showing live webcam feed
2. Real-time FPS counter (top-left)
3. Face detection boxes (green rectangles)
4. Person names with confidence scores
5. Liveness status (REAL/FAKE)
6. Attendance database growing

Problems? Run: python health_check.py
"""

# ============================================================
# GETTING HELP
# ============================================================

HELP = {
    "Quick Start (5 min)": "Read QUICKSTART.md",
    "Full Documentation": "Read README.md",
    "Deployment Help": "Read DEPLOYMENT.md",
    "API Reference": "Read ADVANCED.md",
    "System Issues": "Run python health_check.py",
    "Tests": "Run python test_system.py"
}

# ============================================================
# PRODUCTION DEPLOYMENT CHECKLIST
# ============================================================

DEPLOYMENT_CHECKLIST = """
Before deploying to production:

□ Install all dependencies: pip install -r requirements.txt
□ Register all users: python register.py "Name"
□ Run health check: python health_check.py
□ Test database: python report.py --today
□ Verify camera: python health_check.py > look for "Camera: ✓"
□ Check FPS performance: python main.py (check FPS counter)
□ Backup configuration: cp config/config.yaml config/config.backup.yaml
□ Create daily backup script for database
□ Monitor system resources during operation
□ Set up log rotation for output/system.log
"""

# ============================================================
# PERFORMANCE TIPS
# ============================================================

PERFORMANCE_TIPS = """
To improve performance:

1. GPU Acceleration (if NVIDIA):
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

2. Reduce Frame Size:
   In config.yaml: camera.width = 320, camera.height = 240

3. Use HOG Model:
   In config.yaml: face_recognition.model = 'hog'

4. Reduce Detection Frequency:
   Process every Nth frame instead of every frame

5. Close Unnecessary Programs:
   More system resources = better FPS

Expected Performance:
- CPU: 15-25 FPS
- GPU: 40-100 FPS
"""

# ============================================================
# DATABASE MANAGEMENT
# ============================================================

DATABASE_TIPS = """
SQLite Database Location: database/attendance.db

Backup Database:
    cp database/attendance.db database/attendance_backup.db

Export Attendance:
    python report.py --export

Analyze Records:
    python report.py --stats
    python report.py --person "Name"

Database Schema:
    - attendance table: id, name, timestamp, status, confidence, liveness_status, date, time
    - users table: id, name, registration_time, status

Query Examples:
    sqlite3 database/attendance.db "SELECT * FROM attendance WHERE date='25-12-2024';"
    sqlite3 database/attendance.db "SELECT name, COUNT(*) FROM attendance GROUP BY name;"
"""

# ============================================================
# DAILY OPERATIONS
# ============================================================

DAILY_OPS = """
START OF DAY:
1. python health_check.py    ← Verify system is working
2. python main.py             ← Start the system

DURING DAY:
- System automatically marks attendance
- Monitor FPS (should be 15-30)
- Check for errors in output window

END OF DAY:
1. Press 'q' to quit main.py
2. python report.py --today   ← View today's report
3. python report.py --export  ← Export attendance
4. Backup database manually or via script
5. Review output/system.log for any errors
"""

# ============================================================
# STARTING TEMPLATE CODE
# ============================================================

TEMPLATE_CODE = """
# Example: Access attendance system in your code

from main import FaceAttendanceSystem
from database import AttendanceDatabase
from face_recognition import FaceRecognizer

# Initialize system
system = FaceAttendanceSystem()

# Get statistics
stats = system.recognizer.get_statistics()
print(f"Known people: {stats['unique_persons']}")

# Get today's attendance
db = AttendanceDatabase()
today_count = db.get_today_attendance_count()
print(f"Present today: {today_count}")

# Get specific person's history
attendance_df = db.get_all_attendance(days=30)
person_attendance = attendance_df[attendance_df['name'] == 'John Doe']
print(f"John Doe's attendance: {len(person_attendance)} times")
"""

if __name__ == "__main__":
    print("=" * 70)
    print("FACE RECOGNITION ATTENDANCE SYSTEM - QUICK REFERENCE")
    print("=" * 70)
    
    print("\n📖 DOCUMENTATION FILES:")
    for file, desc in FILES.items():
        if file.endswith(".md"):
            print(f"  → {file}: {desc}")
    
    print("\n⚡ QUICK COMMANDS:")
    for cmd, desc in list(COMMANDS.items())[:5]:
        print(f"  • {desc}: {cmd}")
    
    print("\n⌨️  KEYBOARD SHORTCUTS:")
    for key, desc in SHORTCUTS.items():
        print(f"  • Press {key}: {desc}")
    
    print("\n✅ REQUIREMENTS:")
    for req, val in REQUIREMENTS.items():
        print(f"  • {req}: {val}")
    
    print("\n💡 NEXT STEPS:")
    print("  1. Install: pip install -r requirements.txt")
    print("  2. Register: python register.py \"Your Name\"")
    print("  3. Run: python main.py")
    print("  4. View: python report.py --today")
    
    print("\n📞 HELP:")
    print("  • Problems? Run: python health_check.py")
    print("  • Documentation: Read README.md")
    print("  • API Help: Read ADVANCED.md")
    
    print("\n" + "=" * 70)
