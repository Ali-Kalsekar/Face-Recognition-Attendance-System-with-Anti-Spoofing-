"""
Unit Tests for Face Recognition Attendance System
"""

import unittest
import os
import tempfile
import sqlite3
from datetime import datetime, timedelta
import numpy as np
import cv2

# Import system modules
from database.attendance_db import AttendanceDatabase
from face_detection.face_detector import FaceDetector
from liveness_detection.anti_spoof import AntiSpoofDetector, SimpleLivenessDetector
from utils import FPSCounter, DrawUtils


class TestAttendanceDatabase(unittest.TestCase):
    """Test database operations."""
    
    def setUp(self):
        """Setup test database."""
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.db_path = self.temp_db.name
        self.db = AttendanceDatabase(db_path=self.db_path)
    
    def tearDown(self):
        """Cleanup test database."""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_database_initialization(self):
        """Test database initialization."""
        self.assertTrue(os.path.exists(self.db_path))
    
    def test_mark_attendance(self):
        """Test marking attendance."""
        test_name = "TestUser"
        result = self.db.mark_attendance(test_name, confidence=0.95)
        self.assertTrue(result)
    
    def test_duplicate_prevention(self):
        """Test duplicate prevention."""
        test_name = "TestUser"
        
        # Mark first attendance
        result1 = self.db.mark_attendance(test_name)
        self.assertTrue(result1)
        
        # Try to mark duplicate
        result2 = self.db.mark_attendance(test_name)
        self.assertFalse(result2)  # Should be prevented
    
    def test_user_registration(self):
        """Test user registration."""
        test_name = "NewUser"
        result = self.db.register_user(test_name)
        self.assertTrue(result)
        
        # Try duplicate registration
        result2 = self.db.register_user(test_name)
        self.assertFalse(result2)
    
    def test_get_today_attendance(self):
        """Test getting today's attendance."""
        # Mark multiple attendances
        self.db.mark_attendance("User1")
        self.db.mark_attendance("User2", duplicate_prevention_minutes_override=0)
        self.db.mark_attendance("User3", duplicate_prevention_minutes_override=0)
        
        # Get count
        count = self.db.get_today_attendance_count()
        self.assertEqual(count, 3)


class TestFaceDetector(unittest.TestCase):
    """Test face detection."""
    
    def setUp(self):
        """Setup detector."""
        self.detector = FaceDetector(model_type="haarcascade")
    
    def test_detector_initialization(self):
        """Test detector initialization."""
        self.assertIsNotNone(self.detector)
        self.assertEqual(self.detector.model_type, "haarcascade")
    
    def test_detect_faces_empty_frame(self):
        """Test detection on empty frame."""
        # Create empty frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        faces = self.detector.detect_faces(frame)
        self.assertEqual(len(faces), 0)
    
    def test_detect_faces_invalid_input(self):
        """Test detection with invalid input."""
        faces = self.detector.detect_faces(None)
        self.assertEqual(len(faces), 0)


class TestLivenessDetector(unittest.TestCase):
    """Test liveness detection."""
    
    def setUp(self):
        """Setup detector."""
        self.detector = AntiSpoofDetector(method="blink_motion")
    
    def test_detector_initialization(self):
        """Test detector initialization."""
        self.assertIsNotNone(self.detector)
        self.assertEqual(self.detector.method, "blink_motion")
    
    def test_detect_liveness(self):
        """Test liveness detection."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        is_live, confidence, status = self.detector.detect_liveness(frame)
        
        self.assertIsNotNone(is_live)
        self.assertIsNotNone(confidence)
        self.assertIn(status, ["REAL", "FAKE"])
    
    def test_detector_reset(self):
        """Test detector reset."""
        self.detector.reset()
        self.assertEqual(self.detector.blink_count, 0)


class TestSimpleLivenessDetector(unittest.TestCase):
    """Test simple liveness detector."""
    
    def setUp(self):
        """Setup detector."""
        self.detector = SimpleLivenessDetector()
    
    def test_detector_initialization(self):
        """Test detector initialization."""
        self.assertIsNotNone(self.detector)
    
    def test_detect_liveness_empty_frame(self):
        """Test liveness detection on empty frame."""
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        is_live, confidence, status = self.detector.detect_liveness(frame)
        
        self.assertIsNotNone(is_live)
        self.assertIsNotNone(status)


class TestFPSCounter(unittest.TestCase):
    """Test FPS counter."""
    
    def setUp(self):
        """Setup counter."""
        self.counter = FPSCounter()
    
    def test_counter_initialization(self):
        """Test initialization."""
        self.assertEqual(self.counter.fps, 0)
    
    def test_fps_update(self):
        """Test FPS update."""
        for _ in range(100):
            self.counter.update()
        
        fps = self.counter.get_fps()
        self.assertIsNotNone(fps)


class TestDrawUtils(unittest.TestCase):
    """Test drawing utilities."""
    
    def setUp(self):
        """Setup utilities."""
        self.frame = np.zeros((480, 640, 3), dtype=np.uint8)
    
    def test_draw_face_box(self):
        """Test drawing face box."""
        face = [100, 100, 80, 80]
        result = DrawUtils.draw_face_box(self.frame, face)
        self.assertIsNotNone(result)
    
    def test_draw_text(self):
        """Test drawing text."""
        result = DrawUtils.draw_text(self.frame, "Test", (50, 50))
        self.assertIsNotNone(result)
    
    def test_draw_fps(self):
        """Test drawing FPS."""
        result = DrawUtils.draw_fps(self.frame, 25.5)
        self.assertIsNotNone(result)
    
    def test_draw_unknown_face(self):
        """Test drawing unknown face."""
        face = [100, 100, 80, 80]
        result = DrawUtils.draw_unknown_face(self.frame, face, 0.75)
        self.assertIsNotNone(result)


class TestConfiguration(unittest.TestCase):
    """Test configuration loading."""
    
    def test_config_file_exists(self):
        """Test config file exists."""
        config_path = "./config/config.yaml"
        self.assertTrue(os.path.exists(config_path))


def run_tests():
    """Run all tests."""
    print("="*60)
    print("Running Face Attendance System Tests")
    print("="*60)
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAttendanceDatabase))
    suite.addTests(loader.loadTestsFromTestCase(TestFaceDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestLivenessDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestSimpleLivenessDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestFPSCounter))
    suite.addTests(loader.loadTestsFromTestCase(TestDrawUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestConfiguration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
