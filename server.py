# server.py

import os
from livereload import Server, shell


ROOT_DIR = os.path.abspath(".")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
BUILD_COMMAND = "python main.py"
WATCH_DIRS = ["data", "templates", "static", "src", "doc"]


def main():
    server = Server()
    run_build = shell(BUILD_COMMAND, cwd=ROOT_DIR)
    for folder_name in WATCH_DIRS:
        folder_path = os.path.join(ROOT_DIR, folder_name)
        if os.path.exists(folder_path):
            glob_path = os.path.join(folder_path, "**/*")
            server.watch(glob_path, run_build)
        else:
            print(f"[warning] Folder '{folder_name}' not found, skipping.")
    print(f"[livereload] Serving files from: {DOCS_DIR}")
    server.serve(
        root=DOCS_DIR, 
        port=8000, 
        host='localhost', 
        open_url_delay=1
    )

if __name__ == "__main__":
    main()