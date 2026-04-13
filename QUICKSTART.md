# QUICK START GUIDE

## 5-Minute Setup

### 1. Install Python (if not installed)
- Download from https://www.python.org/
- Make sure to check "Add Python to PATH"

### 2. Navigate to Project
```bash
cd face_attendance_system
```

### 3. Run Setup Script
```bash
python setup.py
```

This will automatically:
- ✓ Create required directories
- ✓ Setup virtual environment
- ✓ Install all dependencies
- ✓ Verify installation

### 4. Register Your First User
```bash
python register.py "Your Name"
```

**During Registration:**
- Position your face in front of camera
- Press SPACE to capture samples (5 minimum)
- Press 'q' to finish

### 5. Run the System
```bash
python main.py
```

**During Execution:**
- Face will be detected automatically
- Attendance marked in database
- Press 'q' to quit

### 6. Check Attendance
```bash
python report.py --today
```

---

## Common Commands

### Register New User
```bash
python register.py "John Doe"
python register.py "Jane Smith" --samples 15
```

### Run Attendance System
```bash
python main.py
```

### View Reports
```bash
python report.py --today          # Today's attendance
python report.py --range 7        # Last 7 days
python report.py --person "Name"  # Person's history
python report.py --stats          # System statistics
```

### Export Data
```bash
python report.py --export
```

---

## Keyboard Controls

### During Main Execution
- **'q'** - Quit application
- **'r'** - Register new user
- **SPACE** - Capture (during registration)

### During Registration
- **SPACE** - Capture face sample
- **'q'** - Quit/Cancel
- **'f'** - Finish early

---

## Troubleshooting

### Issue: Camera Not Working
```bash
# Check if camera is available
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
```

**Solution:** Change `camera: index: 0` to `1` or `2` in `config/config.yaml`

### Issue: Face Not Detected
- Improve lighting
- Move closer to camera
- Try different camera angle
- Increase `confidence_threshold` in config

### Issue: Person Not Recognized
- Register with more samples
- Ensure clear, frontal face images
- Lower `distance_threshold` in config

### Issue: Slow Performance
- Reduce resolution in config
- Use HOG model instead of CNN
- Update GPU drivers for acceleration

---

## Tips for Best Results

1. **Good Lighting** - Bright, even lighting without shadows
2. **Face Position** - Look directly at camera, full frontal view
3. **Distance** - Keep face 30-60cm from camera
4. **No Obstructions** - Remove glasses, hat, or masks if possible
5. **Multiple Angles** - Register from different angles
6. **Clear Background** - Plain background works best

---

## File Locations

```
├── config/config.yaml         ← Edit settings here
├── dataset/known_faces/       ← Registered faces stored here
├── database/attendance.db     ← Attendance records
├── output/attendance_log.csv  ← Exported reports
└── output/system.log          ← System logs
```

---

## Configuration Tips

### Fast Recognition (Default)
```yaml
face_detection:
  model: "haarcascade"
face_recognition:
  model: "hog"
```

### Accurate Recognition
```yaml
face_detection:
  model: "dnn"
face_recognition:
  model: "cnn"
# Warning: Slower but more accurate
```

### Strict Matching
```yaml
face_recognition:
  distance_threshold: 0.4  # Lower = stricter
```

### Relaxed Matching
```yaml
face_recognition:
  distance_threshold: 0.8  # Higher = more permissive
```

---

## Advanced Features

### GPU Acceleration (NVIDIA)
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Print System Info
```bash
python -c "from main import FaceAttendanceSystem; s = FaceAttendanceSystem(); print(s.recognizer.get_statistics())"
```

### Database Backup
```bash
cp database/attendance.db database/attendance_backup.db
```

---

## Need Help?

Check the complete documentation in `README.md`

Common issues section contains solutions for:
- Camera problems
- Detection issues
- Recognition problems
- Performance optimization

---

**Happy Attendance Tracking! 🎉**
