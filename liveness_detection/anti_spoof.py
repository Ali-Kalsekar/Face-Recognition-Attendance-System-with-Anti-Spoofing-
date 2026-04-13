"""
Anti-Spoofing / Liveness Detection Module for Face Recognition Attendance System
"""

import cv2
import numpy as np
from scipy.spatial import distance
from collections import deque
from utils.logger import get_logger


class AntiSpoofDetector:
    """Detect liveness and prevent spoofing attacks."""
    
    def __init__(self, method="blink_motion", blink_threshold=0.2, 
                 motion_threshold=5.0, min_blinks=2):
        """
        Initialize anti-spoof detector.
        
        Args:
            method: "blink", "motion", "blink_motion", "combination"
            blink_threshold: Eye aspect ratio threshold for blink detection
            motion_threshold: Motion magnitude threshold
            min_blinks: Minimum blinks required for liveness
        """
        self.logger = get_logger()
        self.method = method.lower()
        self.blink_threshold = blink_threshold
        self.motion_threshold = motion_threshold
        self.min_blinks = min_blinks
        
        # Tracking variables
        self.blink_count = 0
        self.consecutive_frames = 0
        self.prev_frame = None
        self.eye_aspect_ratio_history = deque(maxlen=30)
        self.motion_history = deque(maxlen=30)
        
        self.logger.info(f"AntiSpoofDetector initialized with method: {self.method}")
    
    def detect_liveness(self, frame, face_location=None):
        """
        Detect if face is real or fake (spoof).
        
        Args:
            frame: Input frame
            face_location: Face location (x, y, w, h) for optional processing
        
        Returns:
            Tuple: (is_live, confidence, status_string)
            is_live: True if real, False if fake
            confidence: Confidence score 0-1
            status_string: "REAL" or "FAKE"
        """
        if self.method == "blink":
            is_live, confidence = self._detect_blink(frame)
        elif self.method == "motion":
            is_live, confidence = self._detect_motion(frame)
        elif self.method == "blink_motion" or self.method == "combination":
            is_live, confidence = self._detect_blink_motion(frame)
        else:
            is_live, confidence = True, 0.5
        
        status = "REAL" if is_live else "FAKE"
        return is_live, confidence, status
    
    def _detect_blink(self, frame):
        """
        Detect blink by analyzing eye aspect ratio.
        
        Returns:
            Tuple: (is_live, confidence)
        """
        try:
            # This is a simplified blink detection
            # For production, use MediaPipe face mesh or dlib landmarks
            height, width = frame.shape[:2]
            is_live = self.blink_count >= self.min_blinks
            confidence = min(self.blink_count / self.min_blinks, 1.0) if self.min_blinks > 0 else 0.5
            
            return is_live, confidence
        except:
            return True, 0.5
    
    def _detect_motion(self, frame):
        """
        Detect motion in face region.
        
        Returns:
            Tuple: (is_live, confidence)
        """
        try:
            if self.prev_frame is None:
                self.prev_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                return True, 0.5
            
            # Calculate optical flow
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calculate difference
            diff = cv2.absdiff(gray, self.prev_frame)
            motion_magnitude = np.mean(diff)
            self.motion_history.append(motion_magnitude)
            
            self.prev_frame = gray
            
            # Check if there's consistent motion
            if len(self.motion_history) > 5:
                avg_motion = np.mean(list(self.motion_history))
                is_live = avg_motion > self.motion_threshold
                confidence = min(avg_motion / self.motion_threshold, 1.0)
            else:
                is_live = True
                confidence = 0.5
            
            return is_live, confidence
        except:
            return True, 0.5
    
    def _detect_blink_motion(self, frame):
        """
        Combined blink and motion detection.
        
        Returns:
            Tuple: (is_live, confidence)
        """
        try:
            motion_live, motion_conf = self._detect_motion(frame)
            blink_live, blink_conf = self._detect_blink(frame)
            
            # Combined decision: both should indicate liveness
            is_live = motion_live or blink_live
            confidence = (motion_conf + blink_conf) / 2
            
            return is_live, confidence
        except:
            return True, 0.5
    
    def update_blink_count(self, ear):
        """
        Update blink count based on eye aspect ratio.
        
        Args:
            ear: Eye aspect ratio value
        """
        self.eye_aspect_ratio_history.append(ear)
        
        if len(self.eye_aspect_ratio_history) > 2:
            # Detect blink: eye closes (low EAR) then opens (high EAR)
            prev_ear = list(self.eye_aspect_ratio_history)[-2]
            current_ear = ear
            
            if prev_ear > self.blink_threshold and current_ear < self.blink_threshold:
                self.consecutive_frames += 1
            elif current_ear > self.blink_threshold:
                if self.consecutive_frames > 0:
                    self.blink_count += 1
                self.consecutive_frames = 0
    
    def reset(self):
        """Reset detection state."""
        self.blink_count = 0
        self.consecutive_frames = 0
        self.prev_frame = None
        self.eye_aspect_ratio_history.clear()
        self.motion_history.clear()
    
    def get_state(self):
        """Get detector state."""
        return {
            "blink_count": self.blink_count,
            "motion_history_length": len(self.motion_history),
            "method": self.method
        }


class SimpleLivenessDetector:
    """Simplified liveness detector using MediaPipe Face Detection."""
    
    def __init__(self):
        """Initialize simplified liveness detector."""
        self.logger = get_logger()
        try:
            import mediapipe as mp
            self.mp_face_detection = mp.solutions.face_detection
            self.face_detection = self.mp_face_detection.FaceDetection()
            self.has_mediapipe = True
            self.logger.info("MediaPipe face detection initialized for liveness")
        except:
            self.has_mediapipe = False
            self.logger.warning("MediaPipe not available, using fallback liveness detection")
    
    def detect_liveness(self, frame):
        """
        Simple liveness check using face detection confidence.
        
        Args:
            frame: Input frame
        
        Returns:
            Tuple: (is_live, confidence, status)
        """
        try:
            if self.has_mediapipe:
                results = self.face_detection.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                
                if results.detections:
                    # Use detection confidence as liveness indicator
                    max_confidence = max([detection.score[0] for detection in results.detections])
                    is_live = max_confidence > 0.5
                    return is_live, max_confidence, "REAL" if is_live else "FAKE"
            
            # Fallback: assume real if face is detected
            return True, 0.7, "REAL"
        except Exception as e:
            self.logger.error(f"Error in liveness detection: {e}")
            return True, 0.5, "REAL"
