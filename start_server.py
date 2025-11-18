import os 
import sys
import subprocess
import time

def start():
    #Change to your project directory if needed
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    subprocess.Popen([
        sys.executable, "manage.py", "runserver", "127.0.0.1:8000", "--noreload"
    ])
    time.sleep(2) #give it time to start
    #Open browser
    import webbrowser
    webbrowser.open("http://127.0.0.1:8000")