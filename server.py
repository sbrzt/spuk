# server.py

import os
from livereload import Server, shell
from src.builder import SiteBuilder


ROOT_DIR = os.path.abspath(".")
DOCS_DIR = os.path.join(ROOT_DIR, "docs")
DEV_ENTITY_LIMIT = 50

BUILD_COMMAND = "python main.py"
WATCH_DIRS = ["data", "templates", "static", "src", "doc"]


def main():
    builder = SiteBuilder()
    builder.load_data()
    builder.build_static()
    builder.build_content(limit=DEV_ENTITY_LIMIT)
    server = Server()

    def on_static_change():
        builder.build_static()
    
    def on_code_change():
        builder.renderer.env.cache = {}
        builder.build_content(limit=DEV_ENTITY_LIMIT)
   
    server.watch(os.path.join(ROOT_DIR, "static/"), on_static_change)
    server.watch(os.path.join(ROOT_DIR, "templates/"), on_code_change)
    #server.watch(os.path.join(ROOT_DIR, "src/"), on_code_change)
    print(f"Serving files from: {DOCS_DIR}")
    server.serve(
        root=DOCS_DIR, 
        port=8000, 
        host='localhost', 
        open_url_delay=1
    )

if __name__ == "__main__":
    main()