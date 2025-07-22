# src/stats_collector.py

from rdflib import Graph, URIRef, RDF
from rdflib.namespace import split_uri
from collections import Counter
from dataclasses import dataclass
from typing import List, Set


@dataclass
class GraphStats:
    total_triples: int
    unique_entities: Set[URIRef]
    unique_properties: Set[URIRef]
    unique_classes: Set[URIRef]
    unique_models: Set[str]
    top_entities: List[tuple]
    top_properties: List[tuple]
    top_classes: List[tuple]
    top_models: List[tuple]


def extract_namespace(uri: URIRef) -> str:
    try:
        ns, _ = split_uri(uri)
        return ns
    except Exception:
        return str(uri)


def collect_graph_stats(graph: Graph) -> GraphStats:
    entities = set()
    properties = set()
    classes = set()
    entity_counter = Counter()
    property_counter = Counter()
    class_counter = Counter()
    model_counter = Counter()
    for s, p, o in graph:
        if isinstance(s, URIRef):
            entities.add(s)
            entity_counter[s] += 1
        if isinstance(o, URIRef):
            if p == RDF.type:
                classes.add(o)
                class_counter[o] += 1
                model_counter[extract_namespace(o)] += 1
            else:
                entities.add(o)
        properties.add(p)
        property_counter[p] += 1
        model_counter[extract_namespace(p)] += 1
    return GraphStats(
        total_triples=len(graph),
        unique_entities=entities,
        unique_properties=properties,
        unique_classes=classes,
        unique_models=set(model_counter.keys()),
        top_entities=entity_counter.most_common(10),
        top_properties=property_counter.most_common(10),
        top_classes=class_counter.most_common(10),
        top_models=model_counter.most_common(10),
    )

