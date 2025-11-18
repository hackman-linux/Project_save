from start_server import start
import webbrowser
import time

if __name__ == "__main__":
    start()
    time.sleep(3)
    webbrowser.open("http://127.0.0.1:8000")