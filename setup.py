"""
Quick Start Guide for Face Recognition Attendance System
Run this to automatically set up the system
"""

import os
import sys
import subprocess
import platform


class SystemSetup:
    """Automated system setup."""
    
    def __init__(self):
        self.system = platform.system()
        self.python_cmd = "python" if self.system == "Windows" else "python3"
    
    def run_command(self, command, description):
        """Run a shell command."""
        print(f"\n{'='*60}")
        print(f"→ {description}")
        print(f"{'='*60}")
        
        try:
            if isinstance(command, str):
                result = subprocess.run(command, shell=True, check=True)
            else:
                result = subprocess.run(command, check=True)
            
            print(f"✓ {description} completed")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Error during {description}: {e}")
            return False
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            return False
    
    def create_directories(self):
        """Create necessary directories."""
        print(f"\n{'='*60}")
        print("→ Creating directories")
        print(f"{'='*60}")
        
        dirs = [
            "dataset/known_faces",
            "models",
            "database",
            "output",
            "config"
        ]
        
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
            print(f"  ✓ Created: {dir_path}")
    
    def setup_venv(self):
        """Setup virtual environment."""
        print(f"\n{'='*60}")
        print("→ Setting up Virtual Environment")
        print(f"{'='*60}")
        
        venv_path = "venv"
        
        if os.path.exists(venv_path):
            response = input("Virtual environment already exists. Recreate? (y/n): ").strip().lower()
            if response != 'y':
                print("Using existing virtual environment")
                return True
            import shutil
            shutil.rmtree(venv_path)
        
        if self.run_command([self.python_cmd, "-m", "venv", venv_path], 
                           "Create virtual environment"):
            print(f"\n✓ Virtual environment created at: {venv_path}")
            return True
        return False
    
    def install_requirements(self):
        """Install Python packages."""
        if self.system == "Windows":
            pip_cmd = ".\\venv\\Scripts\\pip"
        else:
            pip_cmd = "./venv/bin/pip"
        
        return self.run_command([pip_cmd, "install", "-r", "requirements.txt"],
                               "Install Python packages")
    
    def verify_installation(self):
        """Verify installation."""
        print(f"\n{'='*60}")
        print("→ Verifying Installation")
        print(f"{'='*60}")
        
        try:
            import cv2
            print(f"  ✓ OpenCV {cv2.__version__}")
            
            import face_recognition
            print(f"  ✓ face_recognition installed")
            
            import numpy
            print(f"  ✓ NumPy {numpy.__version__}")
            
            import pandas
            print(f"  ✓ Pandas {pandas.__version__}")
            
            import yaml
            print(f"  ✓ PyYAML installed")
            
            import mediapipe
            print(f"  ✓ MediaPipe installed")
            
            print("\n✓ All dependencies verified!")
            return True
        except ImportError as e:
            print(f"✗ Missing dependency: {e}")
            return False
    
    def show_next_steps(self):
        """Show next steps."""
        print(f"\n{'='*60}")
        print("✓ SETUP COMPLETED SUCCESSFULLY!")
        print(f"{'='*60}")
        print("\nNext Steps:")
        print("1. Register users:")
        print(f"   python register.py \"Person Name\"")
        print("\n2. Run the system:")
        print(f"   python main.py")
        print("\n3. View attendance:")
        print(f"   python report.py --today")
        print(f"\n{'='*60}\n")
    
    def run_setup(self):
        """Run complete setup."""
        print("\n" + "="*60)
        print("FACE RECOGNITION ATTENDANCE SYSTEM - SETUP")
        print("="*60)
        
        # Create directories
        self.create_directories()
        
        # Setup virtual environment
        if not self.setup_venv():
            print("✗ Failed to setup virtual environment")
            return False
        
        # Install requirements
        if not self.install_requirements():
            print("✗ Failed to install packages")
            return False
        
        # Verify installation
        if not self.verify_installation():
            print("⚠ Some dependencies may be missing")
            response = input("Continue anyway? (y/n): ").strip().lower()
            if response != 'y':
                return False
        
        # Show next steps
        self.show_next_steps()
        return True


def main():
    """Main setup."""
    try:
        setup = SystemSetup()
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
