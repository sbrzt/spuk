from jinja2 import Environment, FileSystemLoader
from src.utils import escape_html, uri_to_filename, get_uri_label, remove_root, generate_base_path, generate_path
from rdflib import Graph, URIRef, Literal, RDF
from urllib.parse import urlparse
import os

env = Environment(loader=FileSystemLoader("static/templates"))

class DocumentationObject:
    def __init__(self, source, title):
        self.source = source
        self.title = title
        self.base_path = generate_base_path(".")


    def get_source(self):
        return self.source

    def get_title(self):
        return self.title
    
    def get_base_path(self):
        return self.base_path


    def render(self):
        template = env.get_template(f"{self.get_title()}.html")
        return template.render(
            source = self.get_source(),
            title = self.get_title(),
            base_path = self.get_base_path(),
        )

    def save(self, output_dir="docs"):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, f"{self.get_title()}.html"), "w") as f:
            f.write(self.render())
        print(f"✅ Saved query page to {output_dir}/{self.get_title()}.html")
