"""
FPS Counter utility for Face Recognition Attendance System
"""

import time


class FPSCounter:
    """Calculate and display real-time FPS."""
    
    def __init__(self):
        self.fps = 0
        self.prev_time = time.time()
        self.frame_count = 0
        self.fps_update_interval = 10  # Update FPS every N frames
    
    def update(self):
        """Update FPS counter. Call once per frame."""
        self.frame_count += 1
        
        if self.frame_count % self.fps_update_interval == 0:
            current_time = time.time()
            elapsed_time = current_time - self.prev_time
            self.fps = self.fps_update_interval / elapsed_time
            self.prev_time = current_time
            self.frame_count = 0
        
        return self.fps
    
    def get_fps(self):
        """Get current FPS value."""
        return self.fps
    
    def get_frame_time(self):
        """Get average frame time in milliseconds."""
        if self.fps > 0:
            return 1000.0 / self.fps
        return 0
