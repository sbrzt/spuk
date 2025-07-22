# src/path_resolver.py

from rdflib import URIRef
from pathlib import Path
from urllib.parse import urlparse


def uri_to_output_path(uri: URIRef, output_dir: Path) -> Path:
    parsed = urlparse(str(uri))
    parts = parsed.path.strip("/").split("/")
    return output_dir.joinpath(*parts)


def get_entity_output_files(uri: URIRef, output_dir: Path) -> dict:
    entity_dir = uri_to_output_path(uri, output_dir)
    filename = entity_dir.name
    return {
        "dir": entity_dir,
        "html": entity_dir / f"{filename}.html",
        "ttl": entity_dir / f"{filename}.ttl",
        "nt": entity_dir / f"{filename}.nt",
        "xml": entity_dir / f"{filename}.xml",
        "jsonld": entity_dir / f"{filename}.jsonld"
    }
