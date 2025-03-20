from textnode import TextNode
from functions import generate_page
import os
import shutil


def main():
    node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    return node

def copy_static(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
        os.mkdir(destination)
    for file in os.listdir(source):
        source_path = os.path.join(source, file)
        destination_path = os.path.join(destination, file)
        if not os.path.isfile(source_path):
            if not os.path.exists(destination_path):
                os.mkdir(destination_path)
            copy_static(source_path, destination_path)
        else:
            shutil.copy(source_path, destination_path)


copy_static("static", "public")
generate_page("content/index.md", "content/template.html", "public/index.html")