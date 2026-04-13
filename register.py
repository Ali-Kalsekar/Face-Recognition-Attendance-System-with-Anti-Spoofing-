"""
User Registration Script for Face Recognition Attendance System
"""

import cv2
import os
import sys
import argparse
from face_detection import FaceDetector
from utils import get_logger


class UserRegistration:
    """Handle user registration for the system."""
    
    def __init__(self, output_folder="./dataset/known_faces"):
        """
        Initialize registration.
        
        Args:
            output_folder: Folder to save registered faces
        """
        self.logger = get_logger()
        self.output_folder = output_folder
        self.detector = FaceDetector(model_type="haarcascade")
        
        os.makedirs(output_folder, exist_ok=True)
    
    def register_user(self, name, num_samples=5, camera_index=0):
        """
        Register a new user by capturing face images.
        
        Args:
            name: Person name
            num_samples: Number of face samples to capture
            camera_index: Webcam index
        
        Returns:
            True if successful
        """
        self.logger.info(f"Starting registration for: {name}")
        
        # Create user directory
        user_dir = os.path.join(self.output_folder, name)
        
        # Remove existing directory if exists
        if os.path.exists(user_dir):
            response = input(f"User {name} already exists. Overwrite? (y/n): ").strip().lower()
            if response != 'y':
                self.logger.info("Registration cancelled")
                return False
            import shutil
            shutil.rmtree(user_dir)
        
        os.makedirs(user_dir, exist_ok=True)
        
        # Open camera
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            self.logger.error("Failed to open camera")
            return False
        
        sample_count = 0
        skipped_count = 0
        
        print(f"\n{'='*50}")
        print(f"Registering: {name}")
        print(f"{'='*50}")
        print(f"Capturing {num_samples} face samples")
        print(f"Press SPACE to capture a sample")
        print(f"Press 'q' to quit or skip to next")
        print(f"Press 'f' to finish early")
        print(f"{'='*50}\n")
        
        while sample_count < num_samples:
            ret, frame = self.cap.read()
            if not ret:
                self.logger.error("Failed to read frame from camera")
                break
            
            frame = cv2.flip(frame, 1)
            display_frame = frame.copy()
            
            # Detect faces
            faces = self.detector.detect_faces(frame)
            
            if faces:
                # Draw largest face
                face = max(faces, key=lambda f: f[2] * f[3])
                x, y, w, h = face
                cv2.rectangle(display_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(display_frame, "Press SPACE to capture", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                
                status_text = f"Sample: {sample_count}/{num_samples}"
            else:
                cv2.putText(display_frame, "No face detected", (20, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                status_text = f"No face - Skipped: {skipped_count}"
            
            # Draw status
            cv2.putText(display_frame, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            cv2.imshow(f"Registering: {name}", display_frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord(' '):
                if faces:
                    # Save face
                    face = faces[0]
                    x, y, w, h = face
                    face_roi = frame[max(0, y-20):min(frame.shape[0], y+h+20),
                                    max(0, x-20):min(frame.shape[1], x+w+20)]
                    
                    filename = f"{name}_{sample_count}.jpg"
                    filepath = os.path.join(user_dir, filename)
                    cv2.imwrite(filepath, face_roi)
                    
                    sample_count += 1
                    print(f"✓ Captured sample {sample_count}/{num_samples}")
                else:
                    skipped_count += 1
                    print(f"✗ No face detected, skipped")
            
            elif key == ord('q'):
                if sample_count > 0:
                    response = input(f"\nExit with {sample_count} samples? (y/n): ").strip().lower()
                    if response == 'y':
                        break
                else:
                    break
            
            elif key == ord('f'):
                break
        
        cap.release()
        cv2.destroyAllWindows()
        
        if sample_count >= 1:
            self.logger.info(f"Registration completed for {name} with {sample_count} samples")
            print(f"\n✓ Registration completed!")
            print(f"  Saved {sample_count} face samples to {user_dir}")
            return True
        else:
            self.logger.warning(f"Registration failed for {name}: No samples captured")
            import shutil
            shutil.rmtree(user_dir, ignore_errors=True)
            print(f"\n✗ Registration failed: No samples captured")
            return False


def main():
    """Main registration script."""
    parser = argparse.ArgumentParser(description="Register new user for Face Attendance System")
    parser.add_argument("name", help="Person name to register")
    parser.add_argument("--samples", type=int, default=5, help="Number of face samples")
    parser.add_argument("--camera", type=int, default=0, help="Camera index")
    parser.add_argument("--folder", type=str, default="./dataset/known_faces",
                       help="Output folder for face dataset")
    
    args = parser.parse_args()
    
    registration = UserRegistration(output_folder=args.folder)
    success = registration.register_user(args.name, num_samples=args.samples, 
                                        camera_index=args.camera)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
