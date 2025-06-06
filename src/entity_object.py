from jinja2 import Environment, FileSystemLoader
from src.utils import uri_to_filename, remove_root, generate_base_path, generate_path
from rdflib import Graph, URIRef, Literal, RDF
from urllib.parse import urlparse
from src.models import EntityData
from src.knowledge_graph import KnowledgeGraph
import os, tomllib

env = Environment(loader=FileSystemLoader("static/templates"))
with open("config.toml", "rb") as f:
    configuration = tomllib.load(f)

FORMATS = configuration["entity_object"]["formats"]


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
        for itm in FORMATS:
            full_path = os.path.join(self.path, f"{self.filename}.{itm['ext']}")
            self.snippet.serialize(
                destination = full_path,
                format = itm["format"],
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
