"""
Face Recognition Module for Face Recognition Attendance System
"""

import os
import cv2
import numpy as np
from utils.logger import get_logger
import importlib

try:
    _candidate_fr = importlib.import_module("face_recognition")
    if all(
        hasattr(_candidate_fr, attr)
        for attr in ["load_image_file", "face_encodings", "face_distance"]
    ):
        fr = _candidate_fr
        FACE_RECOGNITION_AVAILABLE = True
    else:
        fr = None
        FACE_RECOGNITION_AVAILABLE = False
except Exception:
    fr = None
    FACE_RECOGNITION_AVAILABLE = False


class FaceRecognizer:
    """Recognize faces and identify persons using face_recognition library."""
    
    def __init__(self, dataset_path="./dataset/known_faces", 
                 distance_threshold=0.6, model_type="hog"):
        """
        Initialize face recognizer.
        
        Args:
            dataset_path: Path to known faces dataset
            distance_threshold: Distance threshold for face matching
            model_type: "hog" (faster) or "cnn" (accurate)
        """
        self.logger = get_logger()
        self.dataset_path = dataset_path
        self.distance_threshold = distance_threshold
        self.model_type = model_type
        self.backend = "face_recognition" if FACE_RECOGNITION_AVAILABLE else "opencv_fallback"
        
        # Storage for encodings and names
        self.known_face_encodings = []
        self.known_face_names = []
        
        # Load known faces
        self.load_known_faces()
        
        if FACE_RECOGNITION_AVAILABLE:
            self.logger.info(
                f"FaceRecognizer initialized with backend '{self.backend}' and "
                f"{len(self.known_face_encodings)} known faces"
            )
        else:
            self.logger.warning(
                "face_recognition/dlib is not available. Running in fallback mode; "
                "recognition quality is reduced until dlib is installed."
            )
    
    def load_known_faces(self):
        """Load and encode known faces from dataset."""
        self.known_face_encodings = []
        self.known_face_names = []
        
        if not os.path.exists(self.dataset_path):
            self.logger.warning(f"Dataset path does not exist: {self.dataset_path}")
            return
        
        person_dirs = [d for d in os.listdir(self.dataset_path) 
                      if os.path.isdir(os.path.join(self.dataset_path, d))]
        
        count = 0
        for person_name in person_dirs:
            person_dir = os.path.join(self.dataset_path, person_name)
            image_paths = [
                os.path.join(person_dir, f) for f in os.listdir(person_dir)
                if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))
            ]
            
            for image_path in image_paths:
                try:
                    if FACE_RECOGNITION_AVAILABLE:
                        image = fr.load_image_file(image_path)
                        face_encodings = fr.face_encodings(image)

                        if face_encodings:
                            self.known_face_encodings.append(face_encodings[0])
                            self.known_face_names.append(person_name)
                            count += 1
                    else:
                        image = cv2.imread(image_path)
                        if image is None:
                            continue
                        embedding = self._extract_fallback_embedding(image)
                        self.known_face_encodings.append(embedding)
                        self.known_face_names.append(person_name)
                        count += 1
                except Exception as e:
                    self.logger.warning(f"Error loading image {image_path}: {e}")
        
        self.logger.info(f"Loaded {count} face encodings from dataset")
    
    def recognize_face(self, frame, face_location):
        """
        Recognize a face in the frame.
        
        Args:
            frame: Input frame (BGR)
            face_location: Face location (x, y, w, h)
        
        Returns:
            Tuple: (name, confidence_score) or ("Unknown", 0.0)
        """
        if not self.known_face_encodings:
            return "Unknown", 0.0
        
        try:
            if FACE_RECOGNITION_AVAILABLE:
                return self._recognize_with_face_recognition(frame, face_location)
            return self._recognize_with_fallback(frame, face_location)
        
        except Exception as e:
            self.logger.error(f"Error recognizing face: {e}")
            return "Unknown", 0.0
    
    def recognize_faces_batch(self, frame, face_locations):
        """
        Recognize multiple faces in frame.
        
        Args:
            frame: Input frame
            face_locations: List of face locations
        
        Returns:
            List of tuples: [(name, confidence), ...]
        """
        results = []
        for face_location in face_locations:
            name, confidence = self.recognize_face(frame, face_location)
            results.append((name, confidence))
        
        return results
    
    def add_person(self, name, image_paths):
        """
        Add a new person to known faces.
        
        Args:
            name: Person name
            image_paths: List of image file paths
        
        Returns:
            Number of successfully added encodings
        """
        try:
            added_count = 0
            for image_path in image_paths:
                try:
                    if FACE_RECOGNITION_AVAILABLE:
                        image = fr.load_image_file(image_path)
                        face_encodings = fr.face_encodings(image)

                        if face_encodings:
                            self.known_face_encodings.append(face_encodings[0])
                            self.known_face_names.append(name)
                            added_count += 1
                    else:
                        image = cv2.imread(image_path)
                        if image is None:
                            continue
                        embedding = self._extract_fallback_embedding(image)
                        self.known_face_encodings.append(embedding)
                        self.known_face_names.append(name)
                        added_count += 1
                except Exception as e:
                    self.logger.warning(f"Error adding image {image_path}: {e}")
            
            self.logger.info(f"Added {added_count} encodings for {name}")
            return added_count
        
        except Exception as e:
            self.logger.error(f"Error adding person {name}: {e}")
            return 0
    
    def get_statistics(self):
        """Get recognizer statistics."""
        unique_persons = len(set(self.known_face_names))
        return {
            "total_encodings": len(self.known_face_encodings),
            "unique_persons": unique_persons,
            "distance_threshold": self.distance_threshold,
            "model_type": self.model_type,
            "backend": self.backend,
            "full_recognition_available": FACE_RECOGNITION_AVAILABLE
        }

    def _recognize_with_face_recognition(self, frame, face_location):
        """Recognition path using face_recognition/dlib backend."""
        x, y, w, h = face_location

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_rect = (y, x + w, y + h, x)
        face_encodings = fr.face_encodings(rgb_frame, [face_rect])

        if not face_encodings:
            return "Unknown", 0.0

        face_encoding = face_encodings[0]
        distances = fr.face_distance(self.known_face_encodings, face_encoding)

        if len(distances) == 0:
            return "Unknown", 0.0

        best_match_index = int(np.argmin(distances))
        best_distance = float(distances[best_match_index])

        if best_distance <= self.distance_threshold:
            name = self.known_face_names[best_match_index]
            confidence = max(0.0, min(1.0, 1.0 - best_distance))
            return name, confidence

        return "Unknown", max(0.0, min(1.0, 1.0 - best_distance))

    def _recognize_with_fallback(self, frame, face_location):
        """Fallback recognition using simple OpenCV embedding distance."""
        x, y, w, h = face_location
        roi = frame[max(0, y):max(0, y) + max(1, h), max(0, x):max(0, x) + max(1, w)]
        if roi.size == 0:
            return "Unknown", 0.0

        query_embedding = self._extract_fallback_embedding(roi)
        known = np.array(self.known_face_encodings, dtype=np.float32)
        distances = np.linalg.norm(known - query_embedding, axis=1)

        if distances.size == 0:
            return "Unknown", 0.0

        best_match_index = int(np.argmin(distances))
        best_distance = float(distances[best_match_index])

        # Calibrated threshold for fallback embeddings.
        fallback_threshold = 0.55
        confidence = max(0.0, min(1.0, 1.0 - (best_distance / max(fallback_threshold, 1e-6))))

        if best_distance <= fallback_threshold:
            return self.known_face_names[best_match_index], confidence

        return "Unknown", confidence

    def _extract_fallback_embedding(self, image):
        """Create a lightweight normalized embedding from grayscale face texture."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        normalized = cv2.equalizeHist(gray)
        resized = cv2.resize(normalized, (32, 32), interpolation=cv2.INTER_AREA)
        vector = resized.astype(np.float32).flatten() / 255.0
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm
        return vector
