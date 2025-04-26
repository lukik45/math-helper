import os
import subprocess
import time
import signal
import sys

def start_backend():
    """Start the FastAPI backend server"""
    print("Starting backend server...")
    backend_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    return backend_process

def start_frontend():
    """Start the Streamlit frontend server"""
    print("Starting frontend server...")
    os.environ["API_URL"] = "http://localhost:8000"
    frontend_process = subprocess.Popen(
        ["streamlit", "run", "frontend/Main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    return frontend_process

def main():
    """Run both backend and frontend servers"""
    try:
        # Start backend
        backend_process = start_backend()
        
        # Wait for backend to start
        print("Waiting for backend to start...")
        time.sleep(5)
        
        # Start frontend
        frontend_process = start_frontend()
        
        # Monitor processes
        print("\nAI Math Tutor is running!")
        print("Backend URL: http://localhost:8000")
        print("Frontend URL: http://localhost:8501")
        print("Press Ctrl+C to stop the servers")
        
        # Monitor processes
        try:
            while True:
                if backend_process.poll() is not None:
                    print("Backend server stopped unexpectedly. Restarting...")
                    backend_process = start_backend()
                
                if frontend_process.poll() is not None:
                    print("Frontend server stopped unexpectedly. Restarting...")
                    frontend_process = start_frontend()
                
                time.sleep(1)
        
        except KeyboardInterrupt:
            print("\nStopping servers...")
    
    finally:
        # Clean up processes
        if 'backend_process' in locals() and backend_process:
            backend_process.terminate()
            backend_process.wait()
            print("Backend server stopped.")
        
        if 'frontend_process' in locals() and frontend_process:
            frontend_process.terminate()
            frontend_process.wait()
            print("Frontend server stopped.")

if __name__ == "__main__":
    main()