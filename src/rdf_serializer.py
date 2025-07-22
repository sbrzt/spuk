# src/rdf_serializer.py

from pathlib import Path
from rdflib import Graph, URIRef


class RDFSerializer:

    def __init__(self):
        pass


    def extract_entity_graph(self, entity_uri: URIRef, graph: Graph) -> Graph:
        subgraph = Graph()
        for s, p, o in graph.triples((entity_uri, None, None)):
            subgraph.add((s, p, o))
        for s, p, o in graph.triples((None, None, entity_uri)):
            subgraph.add((s, p, o))
        return subgraph


    def serialize_entity(
        self,
        entity_uri: URIRef,
        graph: Graph,
        output_paths: dict[str, Path]
        ) -> None:
        subgraph = self.extract_entity_graph(entity_uri, graph)
        formats = {
            "ttl": "turtle",
            "xml": "xml",
            "nt": "nt",
            "jsonld": "json-ld"
        }
        for key, rdf_format in formats.items():
            if key in output_paths:
                subgraph.serialize(
                    destination=output_paths[key], 
                    format=rdf_format,
                    encoding="utf-8"
                )
