# src/entity_model.py

from rdflib import Graph, URIRef
from typing import List, Tuple, Generator
from pathlib import Path
from src.path_resolver import get_entity_output_files


class Entity:

    def __init__(
        self, 
        uri: URIRef, 
        graph: Graph
        ):
        self.uri = uri
        self.graph = graph
        self.subject_triples: List[Tuple] = list(graph.triples((uri, None, None)))
        self.object_triples: List[Tuple] = list(graph.triples((None, None, uri)))
    
    @property
    def types(self) -> List[str]:
        return [
            str(o)
            for (_, _, o) in self.graph.triples((self.uri, URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), None))
        ]

    @property
    def triple_count(self) -> int:
        return len(self.subject_triples) + len(self.object_triples)

    @property
    def related_entity_count(self) -> int:
        return len(self.get_related_entities())

    @property
    def subject_triple_count(self) -> int:
        return len(self.subject_triples)

    @property
    def object_triple_count(self) -> int:
        return len(self.object_triples)

    @property
    def render_path(self) -> str:
        return get_entity_output_files(self.uri, Path()).get("html", Path("")).with_suffix("").as_posix()

    def get_predicates_objects(self) -> List[Tuple]:
        return [(p, o) for (_, p, o) in self.subject_triples]

    def get_subjects_predicates(self) -> List[Tuple]:
        return [(s, p) for (s, p, _) in self.object_triples]

    def get_related_entities(self) -> List[URIRef]:
        related = set()
        for (_, p, o) in self.subject_triples:
            if p != URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"):
                if isinstance(o, URIRef):
                    related.add(o)
        for (s, _, _) in self.object_triples:
            if isinstance(s, URIRef):
                related.add(s)
        return list(related)

    def get_entity_subgraph(self) -> Graph:
        subgraph = Graph()
        for triple in self.subject_triples + self.object_triples:
            subgraph.add(triple)
        return subgraph

    def to_turtle(self) -> str:
        return self.get_entity_subgraph().serialize(format="turtle")


def get_entities(graph: Graph) -> Generator[Entity, None, None]:
    seen: Set[URIRef] = set()
    for s in graph.subjects():
        if isinstance(s, URIRef) and s not in seen:
            seen.add(s)
            yield Entity(s, graph)