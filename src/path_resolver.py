# src/path_resolver.py

from rdflib import URIRef
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse, unquote


def uri_to_output_path(uri: URIRef, output_dir: Path) -> Path:
    parsed = urlparse(str(uri))
    parts = [unquote(p) for p in parsed.path.split("/")]
    parts = [p for p in parts if p not in ("", ".", "..") and "/" not in p and "\\" not in p]
    if not parts:
        parts = ["_root"]
    return output_dir.joinpath(*parts)


@lru_cache(maxsize=None)
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
