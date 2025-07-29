import http.server
import socketserver
import threading
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess

WATCH_DIRS = ["data", "templates", "static", "src"]  # Customize this to match your SSG input dirs
WATCH_DIRS = [os.path.abspath(d) for d in WATCH_DIRS if os.path.exists(d)]
PORT = 8000

class RebuildHandler(FileSystemEventHandler):
    def __init__(self, build_command):
        self.build_command = build_command
        self.last_run = 0

    def on_any_event(self, event):
        if event.is_directory:
            return
        now = time.time()
        # Prevent too-frequent builds
        if now - self.last_run < 1:
            return
        print(f"[watch] Detected change in {event.src_path}. Rebuilding...")
        subprocess.run(self.build_command, shell=True)
        self.last_run = now

def start_server():
    os.chdir("docs")  # Serve from docs/
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[serve] Serving at http://localhost:{PORT}")
        httpd.serve_forever()

def start_watcher():
    event_handler = RebuildHandler("python build.py")  # Replace with your build command
    observer = Observer()
    for path in WATCH_DIRS:
        print(f"[watching] {path}")
        observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print(f"[watch] Watching {', '.join(WATCH_DIRS)} for changes.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    # Start HTTP server in separate thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    # Start file watcher
    start_watcher()
