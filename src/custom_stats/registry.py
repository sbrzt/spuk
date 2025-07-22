# src/custom_stats/registry.py

from rdflib import Graph, URIRef
from collections import Counter


def count_by_object(graph: Graph, predicate: URIRef) -> dict:
    counts = Counter()
    for _, p, o in graph.triples((None, predicate, None)):
        counts[o] += 1
    return dict(counts)

STAT_TYPES = {
    "count_by_object": count_by_object
}
