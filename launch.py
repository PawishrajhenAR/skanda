#!/usr/bin/env python3
"""
Launch script for Credit Management System
This script provides an easy way to start the application
"""

import os
import sys
import subprocess
import webbrowser
from time import sleep

def check_dependencies():
    """Check if required dependencies are installed"""
    print("Checking dependencies...")
    
    try:
        import flask
        import flask_sqlalchemy
        import werkzeug
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_application():
    """Start the Flask application"""
    print("Starting Credit Management System...")
    print("=" * 50)
    print("Application will be available at: http://localhost:5000")
    print("Default login credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("=" * 50)
    print("Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Check if venv exists and use its Python interpreter
    venv_python = os.path.join("venv", "Scripts", "python.exe")
    if os.path.exists(venv_python):
        print("Using virtual environment Python interpreter")
        python_exe = venv_python
    else:
        print("WARNING: Virtual environment not found! Using system Python")
        python_exe = sys.executable
    
    try:
        # Start the Flask app
        subprocess.run([python_exe, "app.py"])
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except Exception as e:
        print(f"Error starting application: {e}")

def main():
    """Main function"""
    print("Credit Management System - Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ app.py not found. Please run this script from the project directory.")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Ask user if they want to open browser automatically
    try:
        response = input("Open browser automatically? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            print("Browser will open in 3 seconds...")
            sleep(3)
            webbrowser.open("http://localhost:5000")
    except KeyboardInterrupt:
        print("\nStarting application without opening browser...")
    
    # Start the application
    start_application()

if __name__ == "__main__":
    main()
