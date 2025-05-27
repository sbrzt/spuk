from jinja2 import Environment, FileSystemLoader
from src.utils import escape_html, uri_to_filename, get_uri_label, remove_root, generate_base_path, generate_path
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
        graph_wrapper: KnowledgeGraph
        ):
        self.uri = entity_data.uri
        self.properties = entity_data.properties
        self.types = entity_data.types
        self.path = generate_path(self.uri)
        self.base_path = generate_base_path(self.path)
        self.source_graph = graph_wrapper.get_graph()
        self.snippet = self._extract_snippet()

    def __repr__(self):
        return f"<EntityObject(uri={self.uri})>"

    def _extract_snippet(
        self
        ) -> Graph:
        g = Graph()
        for prefix, namespace in self.source_graph.namespaces():
            g.bind(prefix, namespace)
        entity = URIRef(self.uri)
        for s, p, o in self.source_graph.triples((entity, None, None)):
            g.add((s, p, o))
        return g


    def generate_folders(
        self
        ) -> None:
        os.makedirs(
            self.path, 
            exist_ok=True
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
        filename = uri_to_filename(self.uri)
        for frmt, ext in FORMATS.items():
            full_path = os.path.join(self.path, f"{filename}.{ext}")
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
            base_path = self.base_path,
            path = f"{remove_root(self.path)}/{uri_to_filename(self.uri)}"
        )

    def save(
        self
        ) -> None:
        html = self.render()
        output_path = os.path.join(self.path, f"{uri_to_filename(self.uri)}.html")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
