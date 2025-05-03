from rdflib import Graph, URIRef
from src.utils import get_uri_label, uri_to_filename, get_namespace


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

    def get_summary(self):

        used_namespaces = set()
        for s, p, o in self.graph:
            if isinstance(s, URIRef):
                used_namespaces.add(get_namespace(s))
            used_namespaces.add(get_namespace(p))
            if isinstance(o, URIRef):
                used_namespaces.add(get_namespace(o))

        prefix_map = {str(ns): prefix for prefix, ns in self.graph.namespaces()}
        models_used = [
            (prefix_map[ns], ns) for ns in sorted(used_namespaces) if ns in prefix_map
        ]

        return {
            "num_triples": len(self.graph),
            "num_entities": len(self.entities),
            "models_used": models_used
        }
