# tests/test_stats_collector.py

from rdflib import Graph, URIRef, RDF
from src.stats_collector import collect_graph_stats, extract_namespace


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
    assert stats.unique_models == expected_models
    prop_freqs = dict(stats.top_properties)
    assert prop_freqs[RDF.type] == 5
    for p in graph.predicates():
        assert prop_freqs.get(p, 0) >= 1
    class_freqs = dict(stats.top_classes)
    for cls in stats.unique_classes:
        assert class_freqs[cls] == 5
    top_model_keys = [ns for ns, _ in stats.top_models]
    for model in expected_models:
        assert model in top_model_keys
