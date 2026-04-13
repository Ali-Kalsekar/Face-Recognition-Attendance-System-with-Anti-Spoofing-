"""
Offline Video Processing Module for Face Recognition Attendance System
Process recorded videos to mark attendance
"""

import cv2
import argparse
import os
from face_detection import FaceDetector
from face_recognition import FaceRecognizer
from liveness_detection import SimpleLivenessDetector
from database import AttendanceDatabase
from utils import FPSCounter, DrawUtils, get_logger


class VideoProcessor:
    """Process video files for attendance marking."""
    
    def __init__(self, config=None):
        """Initialize video processor."""
        self.logger = get_logger()
        
        self.detector = FaceDetector(model_type="haarcascade")
        self.recognizer = FaceRecognizer()
        self.liveness_detector = SimpleLivenessDetector()
        self.database = AttendanceDatabase()
        
        self.logger.info("VideoProcessor initialized")
    
    def process_video(self, video_path, output_path=None, save_video=True):
        """
        Process video file and mark attendance.
        
        Args:
            video_path: Path to video file
            output_path: Path to save processed video
            save_video: Whether to save processed video
        
        Returns:
            Statistics dictionary
        """
        self.logger.info(f"Processing video: {video_path}")
        
        if not os.path.exists(video_path):
            self.logger.error(f"Video file not found: {video_path}")
            return None
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            self.logger.error(f"Cannot open video: {video_path}")
            return None
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        self.logger.info(f"Video info: {width}x{height} @ {fps}fps, {total_frames} frames")
        
        # Setup video writer if needed
        if save_video and output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        else:
            out = None
        
        # Statistics
        stats = {
            'total_frames': total_frames,
            'faces_detected': 0,
            'people_recognized': 0,
            'attendance_marked': 0,
            'unique_persons': set()
        }
        
        frame_count = 0
        
        # Process frames
        print(f"\nProcessing video: {video_path}")
        print(f"Total frames: {total_frames}\n")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            output_frame = frame.copy()
            
            # Detect faces
            faces = self.detector.detect_faces(frame)
            
            if faces:
                stats['faces_detected'] += 1
                
                for face in faces:
                    x, y, w, h = face
                    
                    # Recognize
                    name, confidence = self.recognizer.recognize_face(frame, face)
                    
                    if name != "Unknown":
                        stats['people_recognized'] += 1
                        stats['unique_persons'].add(name)
                        
                        # Detect liveness
                        is_live, _, status = self.liveness_detector.detect_liveness(frame)
                        
                        # Mark attendance
                        if is_live and confidence >= 0.6:
                            marked = self.database.mark_attendance(name, confidence, status)
                            if marked:
                                stats['attendance_marked'] += 1
                                self.logger.info(f"Attendance marked: {name}")
                    
                    # Draw on frame
                    if name == "Unknown":
                        DrawUtils.draw_unknown_face(output_frame, face, confidence)
                    else:
                        _, _, status = self.liveness_detector.detect_liveness(frame)
                        DrawUtils.draw_info_on_face(output_frame, face, name, confidence, status)
            
            # Write frame
            if out:
                out.write(output_frame)
            
            # Progress
            if frame_count % max(1, int(fps)) == 0:
                progress = (frame_count / total_frames) * 100
                print(f"Progress: {progress:.1f}% ({frame_count}/{total_frames})")
        
        # Cleanup
        cap.release()
        if out:
            out.release()
        
        stats['unique_persons'] = len(stats['unique_persons'])
        
        self.logger.info(f"Video processing completed")
        self.logger.info(f"Statistics: {stats}")
        
        return stats
    
    def batch_process_videos(self, video_folder, output_folder=None):
        """
        Process all videos in a folder.
        
        Args:
            video_folder: Folder containing videos
            output_folder: Folder to save processed videos
        
        Returns:
            List of processing results
        """
        self.logger.info(f"Starting batch processing from: {video_folder}")
        
        if not os.path.isdir(video_folder):
            self.logger.error(f"Folder not found: {video_folder}")
            return []
        
        # Find video files
        video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv')
        video_files = [f for f in os.listdir(video_folder)
                      if f.lower().endswith(video_extensions)]
        
        if not video_files:
            self.logger.warning(f"No video files found in {video_folder}")
            return []
        
        results = []
        
        for i, video_file in enumerate(video_files, 1):
            print(f"\n{'='*60}")
            print(f"Processing video {i}/{len(video_files)}: {video_file}")
            print(f"{'='*60}")
            
            video_path = os.path.join(video_folder, video_file)
            
            # Output path
            if output_folder:
                os.makedirs(output_folder, exist_ok=True)
                output_path = os.path.join(output_folder, f"processed_{video_file}")
            else:
                output_path = None
            
            # Process
            stats = self.process_video(video_path, output_path, save_video=True)
            
            if stats:
                stats['video_file'] = video_file
                results.append(stats)
                
                print(f"\nResults for {video_file}:")
                print(f"  Faces detected: {stats['faces_detected']}")
                print(f"  People recognized: {stats['people_recognized']}")
                print(f"  Attendance marked: {stats['attendance_marked']}")
                print(f"  Unique persons: {stats['unique_persons']}")
        
        print(f"\n{'='*60}")
        print(f"Batch processing completed")
        print(f"Total videos: {len(results)}")
        print(f"{'='*60}\n")
        
        return results


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Process videos for attendance")
    parser.add_argument("video", help="Video file or folder path")
    parser.add_argument("--output", help="Output file or folder")
    parser.add_argument("--batch", action="store_true", help="Process all videos in folder")
    parser.add_argument("--no-save", action="store_true", help="Don't save processed video")
    
    args = parser.parse_args()
    
    try:
        processor = VideoProcessor()
        
        if args.batch or os.path.isdir(args.video):
            # Batch processing
            results = processor.batch_process_videos(args.video, args.output)
            print(f"Processed {len(results)} videos")
        else:
            # Single video
            stats = processor.process_video(
                args.video,
                output_path=args.output,
                save_video=not args.no_save
            )
            
            if stats:
                print(f"\nProcessing complete!")
                print(f"Faces detected: {stats['faces_detected']}")
                print(f"People recognized: {stats['people_recognized']}")
                print(f"Attendance marked: {stats['attendance_marked']}")
                if args.output and not args.no_save:
                    print(f"Saved to: {args.output}")
    
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
