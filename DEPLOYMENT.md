"""
Deployment and Production Guide
Face Recognition Attendance System
"""

# DEPLOYMENT GUIDE

## Pre-Deployment Checklist

### System Requirements
- [ ] Python 3.8+ installed
- [ ] 4GB+ RAM available
- [ ] Webcam or video input device
- [ ] Stable network connection (for optional cloud features)

### Software Setup
- [ ] All dependencies installed: `pip install -r requirements.txt`
- [ ] Health check passed: `python health_check.py`
- [ ] Users registered: `python register.py "Name"`
- [ ] Database initialized and tested
- [ ] Configuration verified: `config/config.yaml`

### Hardware Verification
- [ ] Camera tested and working
- [ ] Display resolution appropriate
- [ ] Storage space available (20GB recommended for logs)
- [ ] Network connectivity (if remote deployment)

---

## Installation Steps

### Step 1: Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Directory Structure
```bash
# Create required directories
mkdir -p dataset/known_faces
mkdir -p models
mkdir -p database
mkdir -p output
mkdir -p config
```

### Step 3: Register Users
```bash
# Register first user
python register.py "User1" --samples 15

# Register multiple users
python register.py "User2" --samples 10
python register.py "User3" --samples 10
```

### Step 4: Verify Installation
```bash
# Run health check
python health_check.py

# Test main application in debug mode
python main.py
```

---

## Production Deployment

### On Linux Server (Recommended)

```bash
# 1. SSH to server
ssh user@server.address

# 2. Clone/Download application
cd /opt
git clone <repository>
cd face_attendance_system

# 3. Setup environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure systemd service
sudo nano /etc/systemd/system/face-attendance.service
```

**Systemd Service File:**
```ini
[Unit]
Description=Face Recognition Attendance System
After=network.target

[Service]
Type=simple
User=nobody
WorkingDirectory=/opt/face_attendance_system
Environment="PATH=/opt/face_attendance_system/venv/bin"
ExecStart=/opt/face_attendance_system/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 6. Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable face-attendance
sudo systemctl start face-attendance

# Check status
sudo systemctl status face-attendance

# View logs
sudo journalctl -u face-attendance -f
```

---

## Docker Deployment

### Dockerfile Template

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsm6 libxext6 libxrender-dev \
    libopenblas-dev libolapack-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy application
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create directories
RUN mkdir -p dataset/known_faces database output

EXPOSE 8000

CMD ["python", "main.py"]
```

### Build and Run

```bash
# Build image
docker build -t face-attendance .

# Run container
docker run --device /dev/video0 \
           -v $(pwd)/dataset:/app/dataset \
           -v $(pwd)/database:/app/database \
           -v $(pwd)/output:/app/output \
           face-attendance
```

---

## Configuration for Production

### Recommended Settings for Accuracy

```yaml
face_detection:
  model: "dnn"                    # Use DNN for accuracy
  confidence_threshold: 0.7       # Higher precision

face_recognition:
  model: "cnn"                    # Use CNN for recognition
  distance_threshold: 0.55        # Strict matching

liveness_detection:
  method: "blink_motion"          # Combined detection
  min_blinks_required: 3          # Require 3 blinks

database:
  duplicate_prevention_minutes: 240  # 4 hours
```

### Recommended Settings for Speed

```yaml
face_detection:
  model: "haarcascade"            # Fast detection
  confidence_threshold: 0.5

face_recognition:
  model: "hog"                    # Fast recognition
  distance_threshold: 0.65        # Relaxed matching

liveness_detection:
  method: "motion"                # Simple motion check
```

---

## Monitoring and Maintenance

### Daily Checks

```bash
# Check attendance records
python report.py --today

# Export daily report
python report.py --export

# Health check
python health_check.py
```

### Weekly Tasks

```bash
# Backup database
cp database/attendance.db database/attendance_backup_$(date +%Y%m%d).db

# Check logs
grep ERROR output/system.log

# Performance check
# Review FPS and detection rates
```

### Monthly Tasks

```bash
# Analyze attendance patterns
python report.py --range 30

# Archive old records
# Consider archiving records older than 90 days

# Review camera calibration
# Re-register users if recognition accuracy drops
```

---

## Performance Optimization

### CPU Mode (Default)
- Single-threaded, moderate performance
- Suitable for 10-20 concurrent users
- ~20-25 FPS on modern CPU

### GPU Mode (Recommended for Production)
```bash
# Install GPU support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Enable in config
face_recognition:
  model: "cnn"    # GPU accelerated

# Expected performance:
# ~40-60 FPS on NVIDIA GPU
# ~100+ FPS on high-end GPU
```

### Multi-Threading (Advanced)
```python
# Modify main.py for multi-threading
# Separate face detection from recognition
# Use thread pools for parallel processing
```

---

## Database Management

### Backup Procedure

```bash
# Full backup
cp database/attendance.db database/backups/attendance_$(date +%Y%m%d_%H%M%S).db

# Automated daily backup (Linux cron)
0 2 * * * cp /opt/face_attendance_system/database/attendance.db /backups/attendance_$(date +\%Y\%m\%d).db
```

### Data Export

```bash
# Export as CSV
python report.py --export

# Export for specific period
python report.py --range 30 --export

# Import to spreadsheet
# Use output/attendance_log.csv in Excel/Sheets
```

### Database Maintenance

```bash
# Analyze database
sqlite3 database/attendance.db "ANALYZE;"

# Optimize database
sqlite3 database/attendance.db "VACUUM;"

# Check integrity
sqlite3 database/attendance.db "PRAGMA integrity_check;"
```

---

## Troubleshooting Production Issues

### High CPU Usage
- Reduce frame resolution
- Use HOG model instead of CNN
- Reduce detection frequency

### Low Recognition Accuracy
- Re-register problematic users
- Improve lighting conditions
- Adjust distance_threshold down

### Slow Response Time
- Check camera frame rate
- Verify network connectivity
- Monitor system resources

### Database Issues
- Run integrity check
- Backup and optimize database
- Check disk space

---

## Scaling to Multiple Cameras

### Multi-Camera Setup

```python
# Modified main.py for multiple cameras
cameras = [
    {'index': 0, 'name': 'Entrance'},
    {'index': 1, 'name': 'Exit'},
    {'index': 2, 'name': 'Office'}
]

for camera in cameras:
    # Start processing for each camera
```

---

## Security Considerations

1. **Database Security**
   - Backup sensitive data regularly
   - Encrypt database if required
   - Restrict access permissions

2. **Photo Security**
   - Encrypt stored face images
   - Regular security audits
   - GDPR compliance if in EU

3. **Network Security**
   - Use HTTPS for remote access
   - VPN for remote monitoring
   - Firewall configuration

---

## Recovery Procedures

### System Failure Recovery

```bash
# 1. Check database integrity
sqlite3 database/attendance.db "PRAGMA integrity_check;"

# 2. Restore from backup if needed
cp database/attendance_backup.db database/attendance.db

# 3. Restart service
sudo systemctl restart face-attendance

# 4. Verify operation
python health_check.py
```

### Data Recovery
```bash
# If database corrupted:
# 1. Stop application
# 2. Restore latest backup
# 3. Check CSV exports for recovery
# 4. Restart
```

---

## Performance Benchmarks

### Expected Performance (Different Hardware)

| Hardware | FPS | Latency | Recognition Accuracy |
|----------|-----|---------|---------------------|
| CPU (i7) | 15-20 | 100-150ms | 85-95% |
| CPU (i5) | 10-15 | 150-200ms | 85-95% |
| GPU (GTX1060) | 40-50 | 30-50ms | 95-98% |
| GPU (RTX3060) | 80-100 | 15-30ms | 95-98% |

---

## Compliance & Legal

- **GDPR Compliance** - If in EU, ensure compliance for storing face data
- **Data Privacy** - Manage consent for attendance tracking
- **Access Control** - Restrict database access to authorized personnel
- **Audit Trail** - System logs maintain attendance records

---

## Support & Updates

### Check for Updates
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

### Reporting Issues
- Document error in logs
- Run health check
- Collect system information
- Report with reproduction steps

---

**For detailed troubleshooting, see README.md**
