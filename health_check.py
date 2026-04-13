"""
System Health Check and Diagnostics for Face Recognition Attendance System
"""

import cv2
import sys
import os
from datetime import datetime
import platform


class HealthCheck:
    """Perform system health checks."""
    
    def __init__(self):
        self.results = {}
    
    def check_python_version(self):
        """Check Python version."""
        print("\n[1] Checking Python Version...")
        version = platform.python_version()
        major, minor = int(version.split('.')[0]), int(version.split('.')[1])
        
        if major >= 3 and minor >= 8:
            print(f"  ✓ Python {version} (OK)")
            self.results['python'] = True
        else:
            print(f"  ✗ Python {version} (Requires 3.8+)")
            self.results['python'] = False
    
    def check_camera(self):
        """Check camera availability."""
        print("\n[2] Checking Camera...")
        try:
            cap = cv2.VideoCapture(0)
            if cap.isOpened():
                print(f"  ✓ Camera detected and working")
                self.results['camera'] = True
                cap.release()
            else:
                print(f"  ✗ Camera not accessible")
                self.results['camera'] = False
        except Exception as e:
            print(f"  ✗ Camera check failed: {e}")
            self.results['camera'] = False
    
    def check_dependencies(self):
        """Check Python dependencies."""
        print("\n[3] Checking Dependencies...")
        
        dependencies = {
            'opencv-python': 'cv2',
            'face-recognition': 'face_recognition',
            'numpy': 'numpy',
            'pandas': 'pandas',
            'pyyaml': 'yaml',
            'mediapipe': 'mediapipe',
            'torch': 'torch',
            'PIL': 'PIL',
            'scipy': 'scipy'
        }
        
        all_ok = True
        for package, import_name in dependencies.items():
            try:
                module = __import__(import_name)
                version = getattr(module, '__version__', 'unknown')
                print(f"  ✓ {package:<20} {version}")
            except ImportError:
                print(f"  ✗ {package:<20} NOT FOUND")
                all_ok = False
        
        self.results['dependencies'] = all_ok
    
    def check_directories(self):
        """Check required directories."""
        print("\n[4] Checking Directories...")
        
        required_dirs = [
            'dataset/known_faces',
            'database',
            'output',
            'config'
        ]
        
        all_ok = True
        for dir_path in required_dirs:
            if os.path.exists(dir_path):
                print(f"  ✓ {dir_path}")
            else:
                print(f"  ✗ {dir_path} (Missing)")
                all_ok = False
        
        self.results['directories'] = all_ok
    
    def check_database(self):
        """Check database."""
        print("\n[5] Checking Database...")
        
        try:
            from database import AttendanceDatabase
            db = AttendanceDatabase()
            
            today_count = db.get_today_attendance_count()
            print(f"  ✓ Database operational")
            print(f"    - Today's attendance: {today_count}")
            
            self.results['database'] = True
        except Exception as e:
            print(f"  ✗ Database check failed: {e}")
            self.results['database'] = False
    
    def check_config(self):
        """Check configuration."""
        print("\n[6] Checking Configuration...")
        
        try:
            import yaml
            config_path = './config/config.yaml'
            
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                print(f"  ✓ Configuration file found")
                print(f"    - Camera index: {config['camera']['index']}")
                print(f"    - Face detection model: {config['face_detection']['model']}")
                print(f"    - Recognition model: {config['face_recognition']['model']}")
                
                self.results['config'] = True
            else:
                print(f"  ✗ Configuration file not found")
                self.results['config'] = False
        except Exception as e:
            print(f"  ✗ Configuration check failed: {e}")
            self.results['config'] = False
    
    def check_face_detector(self):
        """Check face detection model."""
        print("\n[7] Checking Face Detection...")
        
        try:
            from face_detection import FaceDetector
            detector = FaceDetector()
            print(f"  ✓ Face detector initialized")
            print(f"    - Model: {detector.model_type}")
            
            self.results['face_detector'] = True
        except Exception as e:
            print(f"  ✗ Face detector check failed: {e}")
            self.results['face_detector'] = False
    
    def check_face_recognizer(self):
        """Check face recognition."""
        print("\n[8] Checking Face Recognition...")
        
        try:
            from face_recognition import FaceRecognizer
            recognizer = FaceRecognizer()
            stats = recognizer.get_statistics()
            
            print(f"  ✓ Face recognizer initialized")
            print(f"    - Known encodings: {stats['total_encodings']}")
            print(f"    - Unique persons: {stats['unique_persons']}")
            
            self.results['face_recognizer'] = True
        except Exception as e:
            print(f"  ✗ Face recognizer check failed: {e}")
            self.results['face_recognizer'] = False
    
    def check_gpu(self):
        """Check GPU availability."""
        print("\n[9] Checking GPU Support...")
        
        try:
            import torch
            if torch.cuda.is_available():
                print(f"  ✓ GPU detected: {torch.cuda.get_device_name(0)}")
                print(f"    - CUDA Version: {torch.version.cuda}")
                self.results['gpu'] = True
            else:
                print(f"  ℹ GPU not detected (CPU mode)")
                self.results['gpu'] = False
        except Exception as e:
            print(f"  ℹ GPU check skipped: {e}")
            self.results['gpu'] = False
    
    def generate_report(self):
        """Generate health report."""
        print("\n" + "="*60)
        print("SYSTEM HEALTH REPORT")
        print("="*60)
        
        # Summary
        passed = sum(1 for v in self.results.values() if v)
        total = len(self.results)
        percentage = (passed / total) * 100 if total > 0 else 0
        
        print(f"\nHealth Status: {percentage:.0f}%")
        
        # Detailed results
        print("\nComponent Status:")
        for component, status in self.results.items():
            icon = "✓" if status else "✗"
            print(f"  {icon} {component:<20} {'PASS' if status else 'FAIL'}")
        
        # Recommendations
        print("\nRecommendations:")
        if not self.results.get('camera'):
            print("  • Check camera connection or try different camera index")
        
        if not self.results.get('dependencies'):
            print("  • Run: pip install -r requirements.txt")
        
        if not self.results.get('directories'):
            print("  • Run: python setup.py")
        
        if not self.results.get('gpu'):
            print("  • For GPU support, install CUDA and pytorch with GPU support")
        
        if not self.results.get('face_recognizer'):
            print("  • Register some users with: python register.py \"Name\"")
        
        print("\n" + "="*60)
        
        return percentage >= 80  # System is healthy if 80%+ pass


def main():
    """Run health check."""
    print("\n" + "="*60)
    print("SYSTEM HEALTH CHECK")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    checker = HealthCheck()
    
    checker.check_python_version()
    checker.check_camera()
    checker.check_dependencies()
    checker.check_directories()
    checker.check_config()
    checker.check_database()
    checker.check_face_detector()
    checker.check_face_recognizer()
    checker.check_gpu()
    
    is_healthy = checker.generate_report()
    
    sys.exit(0 if is_healthy else 1)


if __name__ == "__main__":
    main()
