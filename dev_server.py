#!/usr/bin/env python3
import os
import time
import threading
import subprocess
import http.server
import socketserver
from pathlib import Path
from functools import partial
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class SimpleDevServer:
    def __init__(self, port=8001, output_dir="docs"):
        self.port = port
        self.output_dir = output_dir
        self.last_change = 0
        self.is_building = False
        
    def build(self):
        if self.is_building:
            return
            
        self.is_building = True
        try:
            print("🔄 Building...")
            subprocess.run(["python3", "main.py"], check=True)
            print("✅ Build completed!")
            self.notify_reload()
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
        finally:
            self.is_building = False

    def notify_reload(self):
        print("🔄 Notifying browsers to reload...")
        with open(os.path.join(self.output_dir, ".reload"), "w") as f:
            f.write(str(time.time()))
    
    def serve(self):
        handler = partial(http.server.SimpleHTTPRequestHandler, directory=self.output_dir)
        
        try:
            subprocess.run(["fuser", "-k", f"{self.port}/tcp"], 
                          stderr=subprocess.DEVNULL, 
                          stdout=subprocess.DEVNULL)
        except:
            pass
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"🌐 Serving at http://127.0.0.1:{self.port}")
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n🛑 Server stopped")

class FileWatcher(FileSystemEventHandler):
    def __init__(self, dev_server):
        self.dev_server = dev_server
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        if not event.src_path.endswith(('.py', '.html', '.toml')):
            return
            
        current_time = time.time()
        if current_time - self.dev_server.last_change < 1:
            return
            
        print(f"🔍 File changed: {event.src_path}")
        self.dev_server.last_change = current_time
        
        threading.Thread(target=self.dev_server.build, daemon=True).start()

def main():
    dev_server = SimpleDevServer()
    
    print("🚀 Initial build...")
    dev_server.build()
    
    event_handler = FileWatcher(dev_server)
    observer = Observer()
    
    observer.schedule(event_handler, "src", recursive=True)
    observer.schedule(event_handler, "static", recursive=True)
    if os.path.exists("config.toml"):
        observer.schedule(event_handler, "config.toml", recursive=False)
    
    observer.start()
    print("👀 Watching for file changes...")
    
    server_thread = threading.Thread(target=dev_server.serve, daemon=True)
    server_thread.start()
    
    print("✅ Development server ready! Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()