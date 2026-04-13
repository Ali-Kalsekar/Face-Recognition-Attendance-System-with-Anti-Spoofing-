"""
Logger utility for Face Recognition Attendance System
"""

import logging
import os
from datetime import datetime


class SystemLogger:
    """Configure and manage system logging."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SystemLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self.logger = logging.getLogger("FaceAttendance")
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # File handler
        log_dir = "./output"
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, f"system_{datetime.now().strftime('%d_%m_%Y')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%d-%m-%Y %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # Add handlers
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        
        self._initialized = True
    
    def get_logger(self):
        """Get the logger instance."""
        return self.logger


def get_logger():
    """Get logger instance."""
    return SystemLogger().get_logger()
