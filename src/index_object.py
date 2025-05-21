from jinja2 import Environment, FileSystemLoader
from src.utils import escape_html, uri_to_filename, get_uri_label, remove_root, generate_base_path, generate_path
from rdflib import Graph, URIRef, Literal, RDF
from urllib.parse import urlparse
import os

env = Environment(loader=FileSystemLoader("static/templates"))

class IndexObject:
    def __init__(self, entities, summary):
        self.entities = entities
        self.summary = summary
        self.base_path = generate_base_path(".")

    
    def get_entities(self):
        return self.entities

    def get_summary(self):
        return self.summary

    def get_base_path(self):
        return self.base_path


    def render(self):
        template = env.get_template("index.html")
        items = [
            {
                "uri": entity.get_uri(),
                "path": f"{remove_root(entity.get_path())}/{uri_to_filename(entity.get_uri())}",
                "type": entity.get_type(),
            }
            for entity in self.get_entities()
        ]
        return template.render(
            entities = items, 
            summary = self.get_summary(),
            base_path = self.get_base_path()
        )

    def save(self, output_dir="docs"):
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "index.html"), "w") as f:
            f.write(self.render())
        print(f"✅ Saved index page to {output_dir}/index.html")