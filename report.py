"""
Attendance Report Generator for Face Recognition Attendance System
"""

import argparse
import sys
from datetime import datetime
from database import AttendanceDatabase


class AttendanceReporter:
    """Generate and display attendance reports."""
    
    def __init__(self, db_path="./database/attendance.db"):
        """Initialize reporter."""
        self.database = AttendanceDatabase(db_path=db_path)
    
    def show_today_attendance(self):
        """Display today's attendance."""
        print("\n" + "="*60)
        print("TODAY'S ATTENDANCE REPORT")
        print("="*60)
        
        today = datetime.now().strftime("%d-%m-%Y")
        df = self.database.get_attendance_report(today)
        
        if df.empty:
            print("No attendance records for today")
        else:
            print(f"\nDate: {today}")
            print(f"Total Present: {len(df)}\n")
            print(f"{'Name':<20} {'Time':<10} {'Status':<10} {'Confidence':<12} {'Liveness':<10}")
            print("-" * 60)
            
            for _, row in df.iterrows():
                print(f"{row['name']:<20} {row['time']:<10} {row['status']:<10} "
                     f"{row['confidence']:<12.2f} {row['liveness_status']:<10}")
        
        print("="*60 + "\n")
    
    def show_attendance_range(self, days=7):
        """Display attendance for past N days."""
        print("\n" + "="*80)
        print(f"ATTENDANCE REPORT - LAST {days} DAYS")
        print("="*80)
        
        df = self.database.get_all_attendance(days=days)
        
        if df.empty:
            print("No attendance records found")
        else:
            # Group by date and name
            daily_summary = df.groupby('date').size()
            
            print(f"\nTotal Records: {len(df)}")
            print(f"Date Range: Last {days} days\n")
            print(f"{'Date':<12} {'Total Present':<15}")
            print("-" * 30)
            
            for date, count in daily_summary.items():
                print(f"{date:<12} {count:<15}")
            
            # Person summary
            print("\n" + "-"*80)
            print("PERSON-WISE SUMMARY")
            print("-"*80)
            person_summary = df.groupby('name').size().sort_values(ascending=False)
            print(f"\n{'Person Name':<25} {'Attendance Count':<20}")
            print("-" * 45)
            
            for person, count in person_summary.items():
                print(f"{person:<25} {count:<20}")
        
        print("="*80 + "\n")
    
    def export_attendance(self, output_path="./output/attendance_log.csv", date_str=None):
        """Export attendance to CSV."""
        if date_str:
            print(f"Exporting attendance for {date_str}...")
        else:
            print("Exporting today's attendance...")
        
        success = self.database.export_attendance_csv(output_path, date_str)
        
        if success:
            print(f"✓ Attendance exported to: {output_path}")
        else:
            print("✗ Failed to export attendance")
        
        return success
    
    def show_person_history(self, person_name, days=30):
        """Show attendance history for a person."""
        print("\n" + "="*60)
        print(f"ATTENDANCE HISTORY - {person_name}")
        print("="*60)
        
        df = self.database.get_all_attendance(days=days)
        person_df = df[df['name'] == person_name]
        
        if person_df.empty:
            print(f"No attendance records for {person_name}")
        else:
            print(f"\nTotal Attendance: {len(person_df)}")
            print(f"Date Range: Last {days} days\n")
            print(f"{'Date':<12} {'Time':<10} {'Status':<10} {'Confidence':<12}")
            print("-" * 50)
            
            for _, row in person_df.iterrows():
                print(f"{row['date']:<12} {row['time']:<10} {row['status']:<10} "
                     f"{row['confidence']:<12.2f}")
        
        print("="*60 + "\n")
    
    def show_statistics(self):
        """Show overall statistics."""
        print("\n" + "="*60)
        print("SYSTEM STATISTICS")
        print("="*60)
        
        today_count = self.database.get_today_attendance_count()
        all_data = self.database.get_all_attendance(days=365)
        
        print(f"\nToday's Attendance: {today_count}")
        print(f"Total Records (Last 365 days): {len(all_data)}")
        
        if not all_data.empty:
            unique_persons = all_data['name'].nunique()
            print(f"Unique Persons: {unique_persons}")
            
            # Most frequent attendees
            print("\nTop 5 Attendees:")
            top_attendees = all_data['name'].value_counts().head(5)
            for i, (name, count) in enumerate(top_attendees.items(), 1):
                print(f"  {i}. {name}: {count} times")
        
        print("="*60 + "\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Attendance Report Generator")
    parser.add_argument("--today", action="store_true", help="Show today's attendance")
    parser.add_argument("--range", type=int, help="Show attendance for last N days")
    parser.add_argument("--person", type=str, help="Show history for specific person")
    parser.add_argument("--export", action="store_true", help="Export attendance to CSV")
    parser.add_argument("--stats", action="store_true", help="Show system statistics")
    parser.add_argument("--date", type=str, help="Specific date (DD-MM-YYYY)")
    parser.add_argument("--db", type=str, default="./database/attendance.db", 
                       help="Database path")
    
    args = parser.parse_args()
    
    try:
        reporter = AttendanceReporter(db_path=args.db)
        
        if args.today:
            reporter.show_today_attendance()
        elif args.range:
            reporter.show_attendance_range(days=args.range)
        elif args.person:
            reporter.show_person_history(args.person, days=30)
        elif args.export:
            reporter.export_attendance(date_str=args.date)
        elif args.stats:
            reporter.show_statistics()
        else:
            # Show today by default
            reporter.show_today_attendance()
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
