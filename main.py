"""
Face Recognition Attendance System - Main Application
Complete production-ready system with anti-spoofing
"""

import cv2
import yaml
import argparse
import os
import sys
from datetime import datetime
import numpy as np

# Import modules
from face_detection import FaceDetector
from face_recognition import FaceRecognizer
from liveness_detection import SimpleLivenessDetector, AntiSpoofDetector
from database import AttendanceDatabase
from utils import FPSCounter, DrawUtils, get_logger


class FaceAttendanceSystem:
    """Main application class for Face Recognition Attendance System."""
    
    def __init__(self, config_path="./config/config.yaml"):
        """
        Initialize the attendance system.
        
        Args:
            config_path: Path to configuration YAML file
        """
        self.logger = get_logger()
        self.config = self.load_config(config_path)
        
        # Initialize components
        self.logger.info("Initializing Face Attendance System...")
        
        # Face detection
        self.detector = FaceDetector(
            model_type=self.config['face_detection']['model'],
            confidence_threshold=self.config['face_detection']['confidence_threshold']
        )
        
        # Face recognition
        self.recognizer = FaceRecognizer(
            dataset_path=self.config['registration']['output_folder'],
            distance_threshold=self.config['face_recognition']['confidence_threshold'],
            model_type=self.config['face_recognition']['model']
        )
        
        # Liveness detection
        self.liveness_detector = SimpleLivenessDetector()
        
        # Database
        self.database = AttendanceDatabase(
            db_path=self.config['database']['path'],
            duplicate_prevention_minutes=self.config['database']['duplicate_prevention_minutes']
        )
        
        # FPS counter
        self.fps_counter = FPSCounter()
        
        # Video capture
        self.cap = cv2.VideoCapture(self.config['camera']['index'])
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config['camera']['width'])
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config['camera']['height'])
        self.cap.set(cv2.CAP_PROP_FPS, self.config['camera']['fps'])
        
        # Statistics
        self.frame_count = 0
        self.recognized_persons = {}
        
        self.logger.info("System initialized successfully")
    
    def load_config(self, config_path):
        """Load configuration from YAML file."""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                self.logger.info(f"Configuration loaded from {config_path}")
                return config
            else:
                self.logger.warning(f"Config file not found: {config_path}")
                return self.get_default_config()
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration."""
        return {
            'camera': {'index': 0, 'width': 640, 'height': 480, 'fps': 30},
            'face_detection': {'model': 'haarcascade', 'confidence_threshold': 0.5, 'scale_factor': 1.1, 'neighbors': 5},
            'face_recognition': {'model': 'hog', 'confidence_threshold': 0.6, 'distance_threshold': 0.6},
            'liveness_detection': {'method': 'blink_motion', 'blink_threshold': 0.2, 'motion_threshold': 5.0, 'min_blinks_required': 2},
            'database': {'path': './database/attendance.db', 'duplicate_prevention_minutes': 1440},
            'display': {'show_fps': True, 'show_confidence': True, 'show_liveness': True, 'box_color': [0, 255, 0], 'text_color': [255, 255, 255], 'font_scale': 0.6, 'thickness': 2},
            'logging': {'level': 'INFO', 'log_file': './output/system.log'},
            'registration': {'min_samples': 5, 'output_folder': './dataset/known_faces'},
            'system': {'window_name': 'Face Recognition Attendance System', 'quit_key': 'q', 'register_key': 'r', 'record_key': 'space', 'min_frame_size': 20}
        }
    
    def run(self):
        """Main application loop."""
        self.logger.info(f"Starting {self.config['system']['window_name']}")
        recognizer_stats = self.recognizer.get_statistics()
        if not recognizer_stats.get("full_recognition_available", True):
            self.logger.warning(
                "Running in fallback recognition mode (no dlib/face_recognition). "
                "Install dlib + face-recognition for production-grade accuracy."
            )
        
        if not self.cap.isOpened():
            self.logger.error("Failed to open camera")
            return
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    self.logger.error("Failed to read frame")
                    break
                
                self.frame_count += 1
                
                # Flip frame for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Process frame
                processed_frame = self.process_frame(frame)
                
                # Update FPS
                fps = self.fps_counter.update()
                
                # Draw FPS
                if self.config['display']['show_fps']:
                    DrawUtils.draw_fps(processed_frame, fps)
                
                # Display frame
                cv2.imshow(self.config['system']['window_name'], processed_frame)
                
                # Handle keyboard input
                key = cv2.waitKey(1) & 0xFF
                if key == ord(self.config['system']['quit_key']):
                    self.logger.info("Quitting application")
                    break
                elif key == ord(self.config['system']['register_key']):
                    self.register_user_interactive()
        
        except Exception as e:
            self.logger.error(f"Error in main loop: {e}")
        finally:
            self.cleanup()
    
    def process_frame(self, frame):
        """
        Process single frame for attendance.
        
        Args:
            frame: Input frame
        
        Returns:
            Processed frame with visualization
        """
        output_frame = frame.copy()
        height, width = frame.shape[:2]
        
        # Detect faces
        faces = self.detector.detect_faces(
            frame,
            scale_factor=self.config['face_detection']['scale_factor'],
            neighbors=self.config['face_detection']['neighbors']
        )
        
        # Process each detected face
        for face in faces:
            x, y, w, h = face
            
            # Check minimum face size
            if w < self.config['system']['min_frame_size'] or h < self.config['system']['min_frame_size']:
                continue
            
            # Recognize face
            name, confidence = self.recognizer.recognize_face(frame, face)
            
            # Detect liveness
            is_live, liveness_conf, status = self.liveness_detector.detect_liveness(frame)
            
            # Only mark attendance if liveness is detected
            if is_live and confidence >= self.config['face_recognition']['distance_threshold']:
                # Mark attendance
                if name != "Unknown":
                    marked = self.database.mark_attendance(name, confidence, status)
                    if marked:
                        self.logger.info(f"Attendance marked: {name} (Conf: {confidence:.2f})")
                        self.recognized_persons[name] = datetime.now()
            
            # Draw information on frame
            if name == "Unknown":
                DrawUtils.draw_unknown_face(output_frame, face, confidence)
            else:
                DrawUtils.draw_info_on_face(
                    output_frame, face, name, confidence, status,
                    box_color=tuple(self.config['display']['box_color']),
                    text_color=tuple(self.config['display']['text_color'])
                )
        
        # Draw status message
        if len(faces) == 0:
            DrawUtils.draw_status_message(output_frame, "No face detected")
        else:
            DrawUtils.draw_status_message(output_frame, f"Faces detected: {len(faces)}")
        
        return output_frame
    
    def register_user_interactive(self):
        """Register a new user interactively."""
        self.logger.info("Starting user registration...")
        
        name = input("Enter person name: ").strip()
        if not name:
            self.logger.warning("Invalid name")
            return
        
        # Register in database
        self.database.register_user(name)
        
        # Create user directory
        user_dir = os.path.join(self.config['registration']['output_folder'], name)
        os.makedirs(user_dir, exist_ok=True)
        
        # Capture face images
        min_samples = self.config['registration']['min_samples']
        sample_count = 0
        
        self.logger.info(f"Capturing {min_samples} face samples for {name}")
        print(f"\nCapturing face samples for {name}")
        print(f"Press SPACE to capture, 'q' to finish...")
        
        while sample_count < min_samples:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)
            
            # Detect face
            faces = self.detector.detect_faces(frame)
            
            if faces:
                face = faces[0]
                x, y, w, h = face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, f"Samples: {sample_count}/{min_samples}", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow("User Registration", frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' ') and faces:  # Space to capture
                face = faces[0]
                x, y, w, h = face
                face_roi = frame[max(0, y-10):min(frame.shape[0], y+h+10),
                                max(0, x-10):min(frame.shape[1], x+w+10)]
                
                # Save face image
                image_path = os.path.join(user_dir, f"{name}_{sample_count}.jpg")
                cv2.imwrite(image_path, face_roi)
                
                self.logger.info(f"Captured sample {sample_count + 1}")
                print(f"✓ Captured sample {sample_count + 1}/{min_samples}")
                sample_count += 1
            
            elif key == ord('q'):
                break
        
        cv2.destroyWindow("User Registration")
        
        # Reload recognizer with new user
        self.recognizer.load_known_faces()
        self.logger.info(f"User {name} registered successfully with {sample_count} samples")
        print(f"\n✓ User {name} registered successfully with {sample_count} samples!")
    
    def show_statistics(self):
        """Display system statistics."""
        stats = {
            "Total Frames": self.frame_count,
            "Recognized Persons": self.recognizer.get_statistics(),
            "Today's Attendance": self.database.get_today_attendance_count()
        }
        
        self.logger.info("System Statistics:")
        for key, value in stats.items():
            self.logger.info(f"  {key}: {value}")
    
    def cleanup(self):
        """Cleanup resources."""
        try:
            self.logger.info("Cleaning up resources...")
            
            # Export attendance
            self.database.export_attendance_csv()
            
            # Show statistics
            self.show_statistics()
            
            # Release video capture
            if self.cap:
                self.cap.release()
            
            # Close windows
            cv2.destroyAllWindows()
            
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Face Recognition Attendance System")
    parser.add_argument("--config", type=str, default="./config/config.yaml",
                       help="Path to configuration file")
    parser.add_argument("--register", action="store_true", help="Register new user")
    parser.add_argument("--export", action="store_true", help="Export attendance report")
    
    args = parser.parse_args()
    
    try:
        system = FaceAttendanceSystem(config_path=args.config)
        stats = system.recognizer.get_statistics()
        if not stats.get("full_recognition_available", True):
            print("[WARNING] face-recognition/dlib is missing. Running fallback recognition mode.")
            print("          For best accuracy install: pip install dlib face-recognition")
        
        if args.register:
            system.register_user_interactive()
        elif args.export:
            system.database.export_attendance_csv()
            print("✓ Attendance report exported!")
        else:
            # Run main loop
            system.run()
    
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
