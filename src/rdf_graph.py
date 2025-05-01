from rdflib import Graph, URIRef
from src.utils import get_uri_label, uri_to_filename


class RDFGraph:
    def __init__(self, rdf_file: str):
        self.graph = Graph()
        self.graph.parse(rdf_file)
        self.entities = list(set(self.graph.subjects()))
        print(f"🔗 Loaded {len(self.graph)} triples from {rdf_file}")

    def get_entities(self):
        """Return all unique subjects in the RDF graph."""
        return self.entities

    def get_properties(self, subject):
        """Return all (predicate, object) pairs for a given subject."""
        results = []
        for p, o in self.graph.predicate_objects(subject):
            if isinstance(o, URIRef) and o in self.entities:
                results.append({
                    "predicate": get_uri_label(str(p)),
                    "predicate_uri": str(p),
                    "object": get_uri_label(str(o)),
                    "object_uri": uri_to_filename(str(o))
                })
            else:
                results.append({
                    "predicate": get_uri_label(str(p)),
                    "predicate_uri": str(p),
                    "object": get_uri_label(str(o)) if isinstance(o, URIRef) else str(o),
                    "object_uri": str(o) if isinstance(o, URIRef) else None
                })
        return results
