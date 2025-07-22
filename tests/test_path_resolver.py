# tests/test_path_resolver.py

from pathlib import Path
from rdflib import URIRef
from src.path_resolver import uri_to_output_path, get_entity_output_files


def test_uri_to_output_path():
    uri = URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1")
    output_dir = Path("docs")
    expected = Path("docs/changes/4/aldrovandi/pip/foo/1")
    result = uri_to_output_path(uri, output_dir)
    assert result == expected


def test_get_entity_output_files():
    uri = URIRef("https://w3id.org/changes/4/aldrovandi/pip/foo/1")
    output_dir = Path("docs")
    files = get_entity_output_files(uri, output_dir)
    base_dir = Path("docs/changes/4/aldrovandi/pip/foo/1")
    filename = "1"
    assert files["dir"] == base_dir
    assert files["html"] == base_dir / f"{filename}.html"
    assert files["ttl"] == base_dir / f"{filename}.ttl"
    assert files["nt"] == base_dir / f"{filename}.nt"
    assert files["xml"] == base_dir / f"{filename}.xml"
    assert files["jsonld"] == base_dir / f"{filename}.jsonld"
