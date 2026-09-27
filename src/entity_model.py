# src/entity_model.py

from rdflib import Graph, URIRef
from collections import defaultdict
from functools import cached_property
from rdflib import RDF
from typing import List, Tuple, Generator, Set
from pathlib import Path
from src.path_resolver import get_entity_output_files


class Entity:

    def __init__(
        self, 
        uri: URIRef, 
        graph: Graph,
        subject_triples: List[Tuple] = None,
        object_triples: List[Tuple] = None
        ):
        self.uri = uri
        self.graph = graph
        self.subject_triples: List[Tuple] = (
            subject_triples if subject_triples is not None else list(graph.triples((uri, None, None)))
        )
        self.object_triples: List[Tuple] = (
            object_triples if object_triples is not None else list(graph.triples((None, None, uri)))
        )

    @cached_property
    def types(self) -> List[str]:
        return [str(o) for (_, p, o) in self.subject_triples if p == RDF.type]

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

    @cached_property
    def render_path(self) -> str:
        return get_entity_output_files(self.uri, Path()).get("html", Path("")).with_suffix("").as_posix()

    def get_predicates_objects(self) -> List[Tuple]:
        return [(p, o) for (_, p, o) in self.subject_triples]

    def get_subjects_predicates(self) -> List[Tuple]:
        return [(s, p) for (s, p, _) in self.object_triples]

    @cached_property
    def _related_entities(self) -> List[URIRef]:
        related = set()
        for (_, p, o) in self.subject_triples:
            if p != RDF.type:
                if isinstance(o, URIRef) and (o, None, None) in self.graph:
                    related.add(o)
        for (s, _, _) in self.object_triples:
            if isinstance(s, URIRef):
                related.add(s)
        return list(related)

    def get_related_entities(self) -> List[URIRef]:
        return self._related_entities

    @cached_property
    def _subgraph(self) -> Graph:
        subgraph = Graph(bind_namespaces="none")
        for prefix, namespace in self.graph.namespaces():
            subgraph.bind(prefix, namespace, override=False)
        for triple in self.subject_triples + self.object_triples:
            subgraph.add(triple)
        return subgraph

    def get_entity_subgraph(self) -> Graph:
        return self._subgraph

    def to_turtle(self) -> str:
        return self.get_entity_subgraph().serialize(format="turtle")


def get_entities(graph: Graph) -> Generator[Entity, None, None]:
    by_subject = defaultdict(list)
    by_object = defaultdict(list)
    for triple in graph:
        by_subject[triple[0]].append(triple)
        if isinstance(triple[2], URIRef):
            by_object[triple[2]].append(triple)
    for s, triples in by_subject.items():
        if isinstance(s, URIRef):
            yield Entity(s, graph, triples, by_object.get(s, []))
