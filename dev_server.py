#!/usr/bin/env python3
import os
import time
import threading
import subprocess
import http.server
import socketserver
import json
from pathlib import Path
from functools import partial
from urllib.parse import urlparse, parse_qs
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class LiveReloadHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, dev_server=None, **kwargs):
        self.dev_server = dev_server
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        # Handle Server-Sent Events endpoint for live reload
        if self.path == '/dev/reload-stream':
            try:
                encoded = content.encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'text/event-stream')
                self.send_header('Cache-Control', 'no-cache')
                self.send_header('Connection', 'keep-alive')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(encoded)
            except BrokenPipeError:
                print("⚠️ Client disconnected before page was sent (Broken pipe)")
            
            # Add this client to the reload subscribers
            self.dev_server.add_reload_client(self.wfile)
            
            # Keep connection alive
            try:
                while True:
                    time.sleep(1)
                    # Send heartbeat to keep connection alive
                    self.wfile.write(b': heartbeat\n\n')
                    self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                # Client disconnected
                self.dev_server.remove_reload_client(self.wfile)
            return
        
        # For HTML files, inject live reload script
        if self.path.endswith('.html') or self.path == '/':
            try:
                # Get the file path
                if self.path == '/':
                    file_path = os.path.join(self.directory, 'index.html')
                else:
                    file_path = os.path.join(self.directory, self.path.lstrip('/'))
                
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Inject live reload script before closing </body> tag
                    live_reload_script = '''
<script>
(function() {
    if (typeof EventSource !== 'undefined') {
        var source = new EventSource('/dev/reload-stream');
        source.onmessage = function(event) {
            if (event.data === 'reload') {
                console.log('🔄 Live reload triggered');
                window.location.reload();
            }
        };
        source.onerror = function(event) {
            console.log('Live reload connection lost, retrying...');
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        };
        console.log('🔗 Live reload connected');
    }
})();
</script>
</body>'''
                    
                    if '</body>' in content:
                        content = content.replace('</body>', live_reload_script)
                    else:
                        # If no </body> tag, append at the end
                        content += live_reload_script
                    
                    # Send the modified content
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/html; charset=utf-8')
                    self.send_header('Content-Length', len(content.encode('utf-8')))
                    self.end_headers()
                    self.wfile.write(content.encode('utf-8'))
                    return
            except Exception as e:
                print(f"Error injecting live reload script: {e}")
        
        # For all other files, serve normally
        super().do_GET()

class SimpleDevServer:
    def __init__(self, port=8001, output_dir="docs"):
        self.port = port
        self.output_dir = output_dir
        self.last_change = 0
        self.is_building = False
        self.reload_clients = set()
        
    def add_reload_client(self, client):
        """Add a client to receive reload notifications"""
        self.reload_clients.add(client)
        print(f"🔗 Live reload client connected ({len(self.reload_clients)} total)")
    
    def remove_reload_client(self, client):
        """Remove a client from reload notifications"""
        self.reload_clients.discard(client)
        print(f"🔌 Live reload client disconnected ({len(self.reload_clients)} total)")
        
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
        """Send reload signal to all connected browsers"""
        if not self.reload_clients:
            print("📡 Build complete, but no browsers connected for live reload")
            return
            
        print(f"🔄 Notifying {len(self.reload_clients)} browser(s) to reload...")
        
        # Send reload message to all connected clients
        disconnected_clients = set()
        for client in self.reload_clients.copy():
            try:
                client.write(b'data: reload\n\n')
                client.flush()
            except (BrokenPipeError, ConnectionResetError):
                disconnected_clients.add(client)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            self.remove_reload_client(client)
    
    def serve(self):
        # Create handler with reference to dev_server
        handler = partial(LiveReloadHandler, 
                         directory=self.output_dir, 
                         dev_server=self)
        
        try:
            subprocess.run(["fuser", "-k", f"{self.port}/tcp"], 
                          stderr=subprocess.DEVNULL, 
                          stdout=subprocess.DEVNULL)
        except:
            pass
        
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"🌐 Serving at http://127.0.0.1:{self.port}")
            print(f"🔧 Live reload enabled - changes will auto-refresh the browser")
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
    print("💡 Open your browser and live reload will be automatically enabled")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
        observer.stop()
    
    observer.join()

if __name__ == "__main__":
    main()