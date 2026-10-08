# src/stats_collector.py

from rdflib import Graph, URIRef, RDF
from rdflib.namespace import split_uri
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Set
from src.settings import (
    TYPE_PROPERTY,
    N_OBJECTS
)


@dataclass
class GraphStats:
    total_triples: int
    unique_entities: Set[URIRef]
    unique_properties: Set[URIRef]
    unique_classes: Set[URIRef]
    unique_vocabularies: Set[str]
    top_entities: List[tuple]
    top_properties: List[tuple]
    top_classes: List[tuple]
    top_vocabularies: List[tuple]


def extract_namespace(uri: URIRef) -> str:
    uri_str = str(uri)
    try:
        ns, _ = split_uri(uri)
        return str(ns)
    except ValueError:
        if ":" in uri_str:
            prefix = uri_str.split(":")[0]
            return prefix
        return uri_str


def make_shortener(graph: Graph):
    """Return a function labelling a URI "prefix:term" (or "prefix:" for a
    bare namespace) when the graph binds a prefix, the full URI otherwise."""
    prefixes = {str(ns): prefix for prefix, ns in graph.namespaces()}

    def shorten(uri) -> str:
        uri_str = str(uri)
        if uri_str in prefixes:
            return f"{prefixes[uri_str]}:"
        try:
            ns, term = split_uri(uri_str)
        except ValueError:
            return uri_str
        return f"{prefixes[ns]}:{term}" if ns in prefixes else uri_str

    return shorten


def shorten_top(graph: Graph, counter: Counter) -> List[tuple]:
    """Top N entries of a counter, with shortened labels."""
    shorten = make_shortener(graph)
    return [(shorten(uri), count) for uri, count in counter.most_common(N_OBJECTS)]


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
        if isinstance(o, URIRef) and p != RDF.type:
            entities.add(o)
        if p == RDF.type:
            classes.add(o)
            class_counter[o] += 1
            model_counter[extract_namespace(o)] += 1
        properties.add(p)
        if p != RDF.type:
            property_counter[p] += 1
        model_counter[extract_namespace(p)] += 1
        if p == URIRef(TYPE_PROPERTY):
            model_counter[extract_namespace(o)] += 1
    return GraphStats(
        total_triples=len(graph),
        unique_entities=entities,
        unique_properties=properties,
        unique_classes=classes,
        unique_vocabularies=set(model_counter.keys()),
        top_entities=shorten_top(graph, entity_counter),
        top_properties=shorten_top(graph, property_counter),
        top_classes=shorten_top(graph, class_counter),
        top_vocabularies=shorten_top(graph, model_counter),
    )



CARDS = {
    "triples": ("Triples", lambda stats: stats.total_triples),
    "entities": ("Entities", lambda stats: len(stats.unique_entities)),
    "properties": ("Properties", lambda stats: len(stats.unique_properties)),
    "classes": ("Classes", lambda stats: len(stats.unique_classes)),
    "vocabularies": ("Vocabularies", lambda stats: len(stats.unique_vocabularies)),
}

TOP_STATS = ("top_entities", "top_properties", "top_classes", "top_vocabularies")


def build_index_cards(stats: GraphStats, names: List[str]) -> List[Dict]:
    """Resolve the card names configured in [index] to label/value pairs."""
    unknown = [name for name in names if name not in CARDS]
    if unknown:
        raise ValueError(f"Unknown index card(s) {unknown}; available: {sorted(CARDS)}")
    return [{"label": CARDS[name][0], "value": CARDS[name][1](stats)} for name in names]


def build_index_charts(graph: Graph, stats: GraphStats, configs: List[Dict]) -> List[Dict]:
    """Resolve the [[index.charts]] blocks to chart data. Charts with no
    data are dropped rather than rendered as empty cards."""
    charts = []
    for config in configs:
        stat = config["stat"]
        if stat in TOP_STATS:
            data = getattr(stats, stat)
        elif stat == "count_by_object":
            data = shorten_top(graph, Counter(graph.objects(None, URIRef(config["predicate"]))))
        else:
            raise ValueError(f"Unknown chart stat '{stat}'; available: {[*TOP_STATS, 'count_by_object']}")
        if data:
            charts.append({"title": config.get("title", stat), "type": config.get("type", "bar"), "data": data})
    return charts
