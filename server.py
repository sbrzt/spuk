import http.server
import socketserver
import threading
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


ROOT_DIR = os.path.abspath(".")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
WATCH_DIRS = ["data", "templates", "static", "src", "doc"]
WATCH_DIRS = [os.path.abspath(d) for d in WATCH_DIRS if os.path.exists(d)]
PORT = 8000


class RebuildHandler(FileSystemEventHandler):
    def __init__(self, build_command):
        self.build_command = build_command
        self.last_run = 0
        self._debounce_timer = None

    def on_modified(self, event):
        if event.is_directory:
            return
        if not event.src_path.endswith((".ttl", ".jsonld", ".nt", ".html", ".css", ".js", ".md", ".jinja")):
            return

        if self._debounce_timer:
            self._debounce_timer.cancel()
        self._debounce_timer = threading.Timer(0.5, self._rebuild, [event.src_path])
        self._debounce_timer.start()
    
    def _rebuild(self, path):
        now = time.time()
        if now - self.last_run < 1:
            return
        print(f"[watch] Detected change in {path}. Rebuilding...")
        subprocess.run(self.build_command, shell=True, cwd=ROOT_DIR)
        self.last_run = now

def start_server():
    os.chdir(DOCS_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[serve] Serving at http://localhost:{PORT}")
        httpd.serve_forever()

def start_watcher():
    build_command = "python main.py"
    event_handler = RebuildHandler(build_command)
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
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    start_watcher()
