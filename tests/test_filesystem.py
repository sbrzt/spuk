# tests/test_filesystem.py

import pytest
from config import TEMPLATES_DIR
from pathlib import Path
from rdflib import URIRef, Graph
from src.filesystem import (
    ensure_entity_folder_exists,
    write_entity_html,
    write_entity_rdf
)
from src.html_renderer import HTMLRenderer
from src.rdf_serializer import RDFSerializer


class DummyEntity:
    def __init__(self, uri: URIRef):
        self.uri = uri

    def to_dict(self):
        return {
            "uri": str(self.uri),
            "label": "Entity 1"
        }

@pytest.fixture
def parsed_graph():
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
    return graph

@pytest.fixture
def dummy_entity():
    return DummyEntity(URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"))


def test_ensure_entity_folder_exists(tmp_path):
    uri = URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1")
    output_dir = tmp_path / "docs"
    entity_path = output_dir / "changes/4/aldrovandi/pip/foo/1"
    assert not entity_path.exists()
    result_dir = ensure_entity_folder_exists(uri, output_dir)
    assert entity_path.exists()
    assert entity_path.is_dir()
    assert result_dir == entity_path


def test_write_entity_html(tmp_path, dummy_entity):
    renderer = HTMLRenderer(templates_path=Path(TEMPLATES_DIR))
    output_dir = tmp_path / "docs"
    ensure_entity_folder_exists(dummy_entity.uri, output_dir)
    write_entity_html(dummy_entity, output_dir, renderer)
    output_file = output_dir / "changes/4/aldrovandi/pip/foo/1/1.html"
    assert output_file.exists()
    content = output_file.read_text()
    assert "[https://w3id.org/changes/4/aldrovandi/pip/foo/1]" in content


def test_write_entity_rdf(tmp_path, parsed_graph):
    uri = URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1")
    serializer = RDFSerializer()
    output_dir = tmp_path / "docs"
    ensure_entity_folder_exists(uri, output_dir)
    write_entity_rdf(uri, output_dir, parsed_graph, serializer)
    base_path = output_dir / "changes/4/aldrovandi/pip/foo/1/1"
    assert (base_path.with_suffix(".ttl")).exists()
    assert (base_path.with_suffix(".nt")).exists()
    assert (base_path.with_suffix(".xml")).exists()
    assert (base_path.with_suffix(".jsonld")).exists()