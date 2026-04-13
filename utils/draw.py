"""
Drawing utility for visualization in Face Recognition Attendance System
"""

import cv2
import numpy as np


class DrawUtils:
    """Utilities for drawing on video frames."""
    
    @staticmethod
    def draw_face_box(frame, face, color=(0, 255, 0), thickness=2):
        """
        Draw face bounding box.
        
        Args:
            frame: Input frame
            face: Face bounding box (x, y, w, h)
            color: Box color in BGR format
            thickness: Box line thickness
        
        Returns:
            Modified frame
        """
        if face is None or len(face) < 4:
            return frame
        
        x, y, w, h = face
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)
        return frame
    
    @staticmethod
    def draw_text(frame, text, position, font_scale=0.6, thickness=2, 
                  color=(255, 255, 255), bg_color=(0, 0, 0)):
        """
        Draw text with optional background.
        
        Args:
            frame: Input frame
            text: Text to draw
            position: (x, y) position
            font_scale: Font scale
            thickness: Text thickness
            color: Text color in BGR format
            bg_color: Background color (None for no background)
        
        Returns:
            Modified frame
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Get text size
        text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
        x, y = position
        
        # Draw background
        if bg_color is not None:
            cv2.rectangle(
                frame,
                (x - 5, y - text_size[1] - 5),
                (x + text_size[0] + 5, y + 5),
                bg_color,
                -1
            )
        
        # Draw text
        cv2.putText(frame, text, (x, y), font, font_scale, color, thickness)
        return frame
    
    @staticmethod
    def draw_info_on_face(frame, face, name, confidence, liveness_status, 
                         box_color=(0, 255, 0), text_color=(255, 255, 255)):
        """
        Draw complete face information.
        
        Args:
            frame: Input frame
            face: Face bounding box (x, y, w, h)
            name: Person name
            confidence: Recognition confidence (0-1)
            liveness_status: "REAL" or "FAKE"
            box_color: Bounding box color
            text_color: Text color
        
        Returns:
            Modified frame
        """
        if face is None or len(face) < 4:
            return frame
        
        x, y, w, h = face
        
        # Draw face box
        DrawUtils.draw_face_box(frame, face, box_color, 2)
        
        # Determine status color
        if liveness_status == "REAL":
            status_color = (0, 255, 0)  # Green for real
        else:
            status_color = (0, 0, 255)  # Red for fake
        
        # Draw name
        name_text = f"{name}"
        DrawUtils.draw_text(frame, name_text, (x, y - 50), 
                           font_scale=0.7, color=text_color, bg_color=(0, 0, 0))
        
        # Draw confidence
        conf_text = f"Conf: {confidence:.2f}"
        DrawUtils.draw_text(frame, conf_text, (x, y - 25), 
                           font_scale=0.6, color=text_color, bg_color=(0, 0, 0))
        
        # Draw liveness status
        status_text = f"Status: {liveness_status}"
        DrawUtils.draw_text(frame, status_text, (x, y + h + 25), 
                           font_scale=0.6, color=status_color, bg_color=(0, 0, 0))
        
        return frame
    
    @staticmethod
    def draw_fps(frame, fps, position=(10, 30), font_scale=0.7, 
                 thickness=2, color=(0, 255, 0)):
        """
        Draw FPS on frame.
        
        Args:
            frame: Input frame
            fps: FPS value
            position: (x, y) position
            font_scale: Font scale
            thickness: Text thickness
            color: Text color in BGR format
        
        Returns:
            Modified frame
        """
        fps_text = f"FPS: {fps:.1f}"
        DrawUtils.draw_text(frame, fps_text, position, font_scale, thickness, color)
        return frame
    
    @staticmethod
    def draw_unknown_face(frame, face, confidence, box_color=(0, 0, 255)):
        """
        Draw info for unknown face (red box).
        
        Args:
            frame: Input frame
            face: Face bounding box (x, y, w, h)
            confidence: Detection confidence
            box_color: Bounding box color (default red)
        
        Returns:
            Modified frame
        """
        if face is None or len(face) < 4:
            return frame
        
        x, y, w, h = face
        
        # Draw red box for unknown
        DrawUtils.draw_face_box(frame, face, box_color, 2)
        
        # Draw "UNKNOWN"
        DrawUtils.draw_text(frame, "UNKNOWN", (x, y - 25), 
                           font_scale=0.6, color=(0, 0, 255))
        
        # Draw confidence
        conf_text = f"Conf: {confidence:.2f}"
        DrawUtils.draw_text(frame, conf_text, (x, y - 5), 
                           font_scale=0.5, color=(0, 0, 255))
        
        return frame
    
    @staticmethod
    def draw_status_message(frame, message, position=(10, 60), 
                           font_scale=0.7, thickness=2, color=(0, 255, 0)):
        """
        Draw status message on frame.
        
        Args:
            frame: Input frame
            message: Message text
            position: (x, y) position
            font_scale: Font scale
            thickness: Text thickness
            color: Text color
        
        Returns:
            Modified frame
        """
        DrawUtils.draw_text(frame, message, position, font_scale, thickness, 
                           color, bg_color=(0, 0, 0))
        return frame
