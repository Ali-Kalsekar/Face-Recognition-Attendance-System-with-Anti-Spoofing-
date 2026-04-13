"""
Face Detection Module for Face Recognition Attendance System
"""

import cv2
import numpy as np
from utils.logger import get_logger


class FaceDetector:
    """Detect faces in video frames using Haar Cascade or DNN."""
    
    def __init__(self, model_type="dnn", confidence_threshold=0.5):
        """
        Initialize face detector.
        
        Args:
            model_type: "haarcascade" or "dnn"
            confidence_threshold: Minimum detection confidence for DNN
        """
        self.logger = get_logger()
        self.model_type = model_type.lower()
        self.confidence_threshold = confidence_threshold
        
        if self.model_type == "dnn":
            self.init_dnn_detector()
        elif self.model_type == "haarcascade":
            self.init_haarcascade_detector()
        else:
            self.logger.warning(f"Unknown model type: {model_type}, using DNN")
            self.init_dnn_detector()
        
        self.logger.info(f"Face detector initialized with model: {self.model_type}")
    
    def init_dnn_detector(self):
        """Initialize DNN-based face detector (more accurate)."""
        try:
            # DNN model files paths
            modelFile = "./models/opencv_face_detector_uint8.pb"
            configFile = "./models/opencv_face_detector.pbtxt"
            
            # Try to load, if not available use built-in
            try:
                self.net = cv2.dnn.readNetFromTensorflow(configFile, modelFile)
                self.logger.info("Loaded custom DNN model")
            except:
                # Fallback to built-in Caffe model
                self.logger.warning("Custom DNN model not found, using Haar Cascade")
                self.model_type = "haarcascade"
                self.init_haarcascade_detector()
                return
            
            self.nmsThreshold = 0.4
        except Exception as e:
            self.logger.error(f"Error initializing DNN detector: {e}")
            self.init_haarcascade_detector()
    
    def init_haarcascade_detector(self):
        """Initialize Haar Cascade face detector (faster)."""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            
            if self.face_cascade.empty():
                self.logger.error("Failed to load Haar Cascade")
                raise Exception("Haar Cascade not found")
            
            self.logger.info("Haar Cascade detector initialized")
        except Exception as e:
            self.logger.error(f"Error initializing Haar Cascade: {e}")
            raise
    
    def detect_faces(self, frame, scale_factor=1.1, neighbors=5):
        """
        Detect faces in frame.
        
        Args:
            frame: Input frame
            scale_factor: Haar Cascade scale factor
            neighbors: Haar Cascade neighbors
        
        Returns:
            List of faces as [x, y, w, h]
        """
        if frame is None or frame.size == 0:
            return []
        
        try:
            if self.model_type == "dnn":
                return self._detect_faces_dnn(frame)
            else:
                return self._detect_faces_haarcascade(frame, scale_factor, neighbors)
        except Exception as e:
            self.logger.error(f"Error detecting faces: {e}")
            return []
    
    def _detect_faces_haarcascade(self, frame, scale_factor=1.1, neighbors=5):
        """Detect faces using Haar Cascade."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=scale_factor,
            minNeighbors=neighbors,
            minSize=(30, 30)
        )
        
        # Convert to list of [x, y, w, h]
        return [list(face) for face in faces]
    
    def _detect_faces_dnn(self, frame):
        """Detect faces using DNN."""
        height, width = frame.shape[:2]
        
        # Create blob from frame
        blob = cv2.dnn.blobFromImage(
            frame,
            scalefactor=1.0,
            size=(300, 300),
            mean=[104.0, 177.0, 123.0],
            swapRB=False,
            crop=False
        )
        
        self.net.setInput(blob)
        detections = self.net.forward()
        
        faces = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            
            if confidence > self.confidence_threshold:
                box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
                x1, y1, x2, y2 = box.astype(int)
                
                x = max(0, x1)
                y = max(0, y1)
                w = min(width - x, x2 - x1)
                h = min(height - y, y2 - y1)
                
                if w > 0 and h > 0:
                    faces.append([x, y, w, h])
        
        return faces
    
    def get_detector_info(self):
        """Get detector information."""
        return {
            "model_type": self.model_type,
            "confidence_threshold": self.confidence_threshold
        }
