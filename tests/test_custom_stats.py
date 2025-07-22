# tests/test_custom_stats.py

from rdflib import Graph
from src.custom_stats.engine import load_custom_stats
import tempfile
import shutil
from pathlib import Path


def test_load_custom_stats():
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
    temp_dir = tempfile.mkdtemp()
    config_path = Path(temp_dir) / "config.yaml"
    config_yaml = """
custom_stats:
  - name: "status_counts"
    label: "Status Breakdown"
    type: "count_by_object"
    predicate: "http://w3id.org/sche/ma/status"
"""
    config_path.write_text(config_yaml)
    try:
        stats = load_custom_stats(graph, config_path=config_path)
        assert "status_counts" in stats
        assert stats["status_counts"]["label"] == "Status Breakdown"
        data = stats["status_counts"]["data"]
        expected = {
            "active": 2,
            "inactive": 1,
            "published": 1,
            "archived": 1,
        }
        str_data = {str(k): v for k, v in data.items()}
        assert str_data == expected
    finally:
        shutil.rmtree(temp_dir)
