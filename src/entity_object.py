from jinja2 import Environment, FileSystemLoader
from src.utils import uri_to_filename, remove_root, generate_base_path, generate_path
from rdflib import Graph, URIRef, Literal, RDF
from urllib.parse import urlparse
from src.models import EntityData
from src.knowledge_graph import KnowledgeGraph
import os

env = Environment(loader=FileSystemLoader("static/templates"))

class EntityObject:
    def __init__(
        self,
        entity_data: EntityData,
        ):
        self.uri = entity_data.uri
        self.properties = entity_data.properties
        self.types = entity_data.types
        self.path = generate_path(self.uri)
        self.filename = uri_to_filename(self.uri)
        self.render_path = f"{remove_root(self.path)}/{self.filename}"

        #print(f"self.path: {self.path}")
        #print(f"self.filename: {self.filename}")
        #print(f"render_path: {self.render_path}")

        self.snippet = entity_data.snippet

    def __repr__(self):
        return f"<EntityObject(uri={self.uri})>"


    def generate_folders(
        self
        ) -> None:
        os.makedirs(
            self.path, 
            exist_ok = True
            )
    
    def serialize(
        self
        ) -> None:
        FORMATS = {
            "turtle": "ttl",
            "nt": "nt",
            "xml": "xml",
            "json-ld": "jsonld"
        }
        for frmt, ext in FORMATS.items():
            full_path = os.path.join(self.path, f"{self.filename}.{ext}")
            self.snippet.serialize(
                destination = full_path,
                format = frmt,
                encoding = "utf-8"
            )
    
    def render(
        self
        ) -> str:
        template = env.get_template("entity.html")
        return template.render(
            entity_uri = self.uri,
            entity_types = self.types,
            property_object_pairs = self.properties,
            path = self.render_path
        )

    def save(
        self
        ) -> None:
        html = self.render()
        output_path = os.path.join(self.path, f"{self.filename}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
