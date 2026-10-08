# tests/test_stats_collector.py

from rdflib import Graph, URIRef, RDF
import pytest
from src.stats_collector import collect_graph_stats, build_index_cards, build_index_charts


def test_collect_graph_stats():
    graph = Graph()
    TEST_GRAPH = """
# tests/data/test_graph.ttl

@prefix ex: <http://example.org/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix sche: <http://w3id.org/sche/ma/> .

<https://w3id.org/changes/4/aldrovandi/pip/foo/1>
    a ex:Entity ;
    rdfs:label "Entity foo 1" ;
    sche:status "active" .

<https://w3id.org/changes/4/aldrovandi/pip/foo/2>
    a ex:Entity ;
    rdfs:label "Entity foo 2" ;
    sche:status "inactive" .

<https://w3id.org/changes/4/aldrovandi/pip/1>
    a ex:Entity ;
    rdfs:label "Entity pip 1" ;
    sche:status "active" .

<https://w3id.org/changes/4/aldrovandi/bub/foo/gog/1>
    a ex:Entity ;
    rdfs:label "Entity bub gog 1" ;
    sche:status "published" .

<https://w3id.org/changes/4/aldrovandi/pip/01/1>
    a ex:Entity ;
    rdfs:label "Entity pip 01 1" ;
    sche:status "archived" .    
"""
    graph.parse(data=TEST_GRAPH, format="turtle")
    stats = collect_graph_stats(graph)
    assert stats.total_triples == 15
    assert len(stats.unique_entities) == 5
    assert len(stats.unique_properties) == 3
    assert len(stats.unique_classes) == 1
    expected_models = {
        "http://example.org/",
        "http://www.w3.org/2000/01/rdf-schema#",
        "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "http://w3id.org/sche/ma/",
    }
    assert stats.unique_vocabularies == expected_models
    prop_freqs = dict(stats.top_properties)
    assert prop_freqs == {"rdfs:label": 5, "sche:status": 5}
    assert dict(stats.top_classes) == {"ex:Entity": 5}
    assert {ns for ns, _ in stats.top_vocabularies} == {"ex:", "rdfs:", "rdf:", "sche:"}
    assert all(uri.startswith("https://") for uri, _ in stats.top_entities)

    cards = build_index_cards(stats, ["triples", "classes"])
    assert cards == [{"label": "Triples", "value": 15}, {"label": "Classes", "value": 1}]
    with pytest.raises(ValueError):
        build_index_cards(stats, ["nope"])

    charts = build_index_charts(graph, stats, [
        {"stat": "top_classes", "title": "Classes"},
        {"stat": "count_by_object", "predicate": "http://w3id.org/sche/ma/status", "type": "line"},
        {"stat": "count_by_object", "predicate": "http://example.org/unused"},
    ])
    assert charts[0] == {"title": "Classes", "type": "bar", "data": [("ex:Entity", 5)]}
    assert charts[1]["type"] == "line"
    assert dict(charts[1]["data"]) == {"active": 2, "inactive": 1, "published": 1, "archived": 1}
    assert len(charts) == 2  # chart with no data is dropped
    with pytest.raises(ValueError):
        build_index_charts(graph, stats, [{"stat": "nope"}])
