from jinja2 import Environment, FileSystemLoader
from src.utils import escape_html, uri_to_filename, get_uri_label, remove_root, generate_base_path, generate_path
from rdflib import Graph, URIRef, Literal, RDF
from urllib.parse import urlparse
import os

env = Environment(loader=FileSystemLoader("static/templates"))

class EntityObject:
    def __init__(self, uri, property_object_pairs, source):
        self.uri = uri
        self.type = None
        self.property_object_pairs = property_object_pairs
        self.source = source
        self.path = generate_path(self.uri)
        self.rdf = self.generate_rdf()
        self.base_path = generate_base_path(self.get_path())

    
    def generate_path(self):
        root = "docs"
        path = urlparse(self.get_uri()).path
        parts = path.strip("/").split("/")
        full_path = os.path.join(root, *parts)
        return full_path

    def generate_folders(self):
        os.makedirs(self.get_path(), exist_ok=True)

    def generate_rdf(self):
        source = self.source.graph
        g = Graph()
        for prefix, namespace in source.namespaces():
            g.bind(prefix, namespace)
        for s, p, o in source.triples((URIRef(self.get_uri()), None, None)):
            g.add((s, p, o))
            if p == RDF.type:
                self.type = str(o)
        return g


    def get_uri(self):
        return self.uri

    def get_path(self):
        return self.path

    def get_property_object_pairs(self):
        return self.property_object_pairs

    def get_rdf(self):
        return self.rdf
    
    def get_type(self):
        return self.type

    def get_base_path(self):
        return self.base_path

    
    def serialize(self):
        formats = {
            "turtle": "ttl",
            "nt": "nt",
            "xml": "xml",
            "json-ld": "jsonld"
        }
        for frmt, ext in formats.items():
            rdf = self.get_rdf()
            filename = uri_to_filename(self.get_uri())
            full_path = os.path.join(self.get_path(), f"{filename}.{ext}")
            rdf.serialize(
                destination=full_path, 
                format=frmt,
                encoding="utf-8"
            )


    def render(self):
        template = env.get_template("entity.html")
        return template.render(
            entity_uri = self.get_uri(),
            entity_type = self.get_type(),
            property_object_pairs = self.get_property_object_pairs(),
            base_path = self.get_base_path(),
            path = f"{remove_root(self.get_path())}/{uri_to_filename(self.get_uri())}"
        )

    def save(self):
        """Saves the HTML page to the output directory."""
        html = self.render()
        output_path = os.path.join(self.get_path(), f"{uri_to_filename(self.get_uri())}.html")
        with open(output_path, "w") as f:
            f.write(html)
