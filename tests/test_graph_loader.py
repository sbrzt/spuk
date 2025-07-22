# tests/text_graph_loader.py

import pytest
from rdflib import URIRef, Graph
from src.graph_loader import load_graph
from pathlib import Path
from unittest.mock import patch, MagicMock


def test_load_graph_from_file():
    source = {
        "type": "file",
        "file_path": Path("tests/data/test_graph.ttl"),
        "file_format": "turtle"
    }
    graph = load_graph(source)
    assert len(graph) > 0
    assert (URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1"), None, None) in graph


@patch("src.graph_loader.SPARQLWrapper")
def test_load_graph_from_sparql(mock_sparql_wrapper):
    turtle_data = """
    @prefix ex: <http://example.org/> .
    <https://w3id.org/changes/4/aldrovandi/pip/foo/2> a ex:Type ;
               ex:label "Entity 2" .
    """
    mock_instance = MagicMock()
    mock_instance.query.return_value.convert.return_value = turtle_data
    mock_sparql_wrapper.return_value = mock_instance
    source = {
        "type": "sparql",
        "sparql_endpoint": "http://fake-sparql-endpoint.org"
    }
    graph = load_graph(source)
    assert isinstance(graph, Graph)
    assert len(graph) > 0
    assert (URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/2"), None, None) in graph
