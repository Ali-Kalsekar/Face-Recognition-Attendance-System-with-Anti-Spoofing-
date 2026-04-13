"""
Attendance Database Module for Face Recognition Attendance System
"""

import sqlite3
import os
from datetime import datetime, timedelta
import pandas as pd
from utils.logger import get_logger


class AttendanceDatabase:
    """Manage attendance records in SQLite database."""
    
    def __init__(self, db_path="./database/attendance.db", 
                 duplicate_prevention_minutes=1440):
        """
        Initialize database.
        
        Args:
            db_path: Path to SQLite database
            duplicate_prevention_minutes: Minutes to prevent duplicate entries (default 24 hours)
        """
        self.logger = get_logger()
        self.db_path = db_path
        self.duplicate_prevention_minutes = duplicate_prevention_minutes
        
        # Create directory if not exists
        os.makedirs(os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True)
        
        # Initialize database
        self.init_database()
        
        self.logger.info(f"Database initialized at {db_path}")
    
    def init_database(self):
        """Initialize database tables."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create attendance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'Present',
                    confidence REAL,
                    liveness_status TEXT DEFAULT 'REAL',
                    date TEXT NOT NULL,
                    time TEXT NOT NULL
                )
            ''')
            
            # Create users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    registration_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'Active'
                )
            ''')
            
            # Create index for faster queries
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_name_timestamp ON attendance(name, timestamp)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_date ON attendance(date)')
            
            conn.commit()
            conn.close()
            
            self.logger.info("Database tables created successfully")
        except Exception as e:
            self.logger.error(f"Error initializing database: {e}")
            raise
    
    def mark_attendance(self, name, confidence=0.0, liveness_status="REAL"):
        """
        Mark attendance for a person with duplicate prevention.
        
        Args:
            name: Person name
            confidence: Recognition confidence score
            liveness_status: "REAL" or "FAKE"
        
        Returns:
            True if attendance marked, False if duplicate
        """
        try:
            # Check for duplicate entry
            if self.has_recent_entry(name):
                self.logger.warning(f"Duplicate entry prevented for {name}")
                return False
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now()
            date_str = now.strftime("%d-%m-%Y")
            time_str = now.strftime("%H:%M:%S")
            
            cursor.execute('''
                INSERT INTO attendance (name, timestamp, status, confidence, liveness_status, date, time)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (name, now, "Present", confidence, liveness_status, date_str, time_str))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Attendance marked for {name}: {date_str} {time_str}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error marking attendance: {e}")
            return False
    
    def has_recent_entry(self, name):
        """
        Check if person has recent attendance entry.
        
        Args:
            name: Person name
        
        Returns:
            True if recent entry exists, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cutoff_time = datetime.now() - timedelta(minutes=self.duplicate_prevention_minutes)
            
            cursor.execute('''
                SELECT COUNT(*) FROM attendance
                WHERE name = ? AND timestamp > ?
            ''', (name, cutoff_time))
            
            count = cursor.fetchone()[0]
            conn.close()
            
            return count > 0
        except Exception as e:
            self.logger.error(f"Error checking recent entry: {e}")
            return False
    
    def register_user(self, name):
        """
        Register a new user in database.
        
        Args:
            name: Person name
        
        Returns:
            True if registered, False if already exists
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO users (name) VALUES (?)', (name,))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"User registered: {name}")
            return True
        except sqlite3.IntegrityError:
            self.logger.warning(f"User already exists: {name}")
            return False
        except Exception as e:
            self.logger.error(f"Error registering user: {e}")
            return False
    
    def get_attendance_report(self, date_str=None):
        """
        Get attendance report for specific date.
        
        Args:
            date_str: Date string in format "DD-MM-YYYY" (None for today)
        
        Returns:
            DataFrame with attendance records
        """
        try:
            if date_str is None:
                date_str = datetime.now().strftime("%d-%m-%Y")
            
            conn = sqlite3.connect(self.db_path)
            
            query = 'SELECT name, time, status, confidence, liveness_status FROM attendance WHERE date = ? ORDER BY time'
            df = pd.read_sql_query(query, conn, params=(date_str,))
            
            conn.close()
            
            return df
        except Exception as e:
            self.logger.error(f"Error getting attendance report: {e}")
            return pd.DataFrame()
    
    def get_all_attendance(self, days=30):
        """
        Get all attendance records from last N days.
        
        Args:
            days: Number of days to retrieve
        
        Returns:
            DataFrame with attendance records
        """
        try:
            conn = sqlite3.connect(self.db_path)
            
            cutoff_date = datetime.now() - timedelta(days=days)
            query = 'SELECT * FROM attendance WHERE timestamp > ? ORDER BY timestamp DESC'
            df = pd.read_sql_query(query, conn, params=(cutoff_date,))
            
            conn.close()
            
            return df
        except Exception as e:
            self.logger.error(f"Error getting all attendance: {e}")
            return pd.DataFrame()
    
    def export_attendance_csv(self, output_path="./output/attendance_log.csv", date_str=None):
        """
        Export attendance to CSV file.
        
        Args:
            output_path: Path to save CSV file
            date_str: Date string (None for today)
        
        Returns:
            True if successful
        """
        try:
            df = self.get_attendance_report(date_str)
            
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
            df.to_csv(output_path, index=False)
            
            self.logger.info(f"Attendance exported to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting attendance: {e}")
            return False
    
    def get_today_attendance_count(self):
        """Get count of people present today."""
        try:
            today = datetime.now().strftime("%d-%m-%Y")
            df = self.get_attendance_report(today)
            return len(df)
        except:
            return 0
    
    def get_today_attendance_list(self):
        """Get list of people present today."""
        try:
            today = datetime.now().strftime("%d-%m-%Y")
            df = self.get_attendance_report(today)
            return df['name'].tolist() if not df.empty else []
        except:
            return []
    
    def close(self):
        """Close database connection."""
        self.logger.info("Database connection closed")
