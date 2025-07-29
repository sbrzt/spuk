# src/filesystem.py

import os
import shutil
from pathlib import Path
from rdflib import URIRef, Graph
from typing import List
from src.path_resolver import get_entity_output_files
from src.html_renderer import HTMLRenderer
from src.rdf_serializer import RDFSerializer
from src.entity_model import Entity


def ensure_entity_folder_exists(uri: URIRef, output_dir: Path) -> Path:
    paths = get_entity_output_files(uri, output_dir)
    entity_dir = paths["dir"]
    entity_dir.mkdir(parents=True, exist_ok=True)
    return entity_dir


def write_html_file(content: str, output_path: Path) -> None:
    output_path.write_text(content, encoding="utf-8")


def write_index_html(output_dir: Path, renderer: HTMLRenderer, stats, custom_stats=None) -> None:
    html_content = renderer.render_index(stats, custom_stats)
    output_path = output_dir / "index.html"
    write_html_file(html_content, output_path)


def write_query_html(output_dir: Path, renderer: HTMLRenderer) -> None:
    html_content = renderer.render_query()
    output_path = output_dir / "query.html"
    write_html_file(html_content, output_path)


def write_entities_html(entities: List[Entity], output_dir: Path, renderer: HTMLRenderer) -> None:
    html_content = renderer.render_entities(entities)
    output_path = output_dir / "entities.html"
    write_html_file(html_content, output_path)


def write_entity_html(entity, output_dir: Path, renderer: HTMLRenderer) -> None:
    paths = get_entity_output_files(entity.uri, output_dir)
    html_content = renderer.render_entity(entity)
    write_html_file(html_content, paths["html"])


def write_entity_rdf(entity_uri: URIRef, output_dir: Path, graph: Graph, serializer: RDFSerializer) -> None:
    paths = get_entity_output_files(entity_uri, output_dir)
    serializer.serialize_entity(
        entity_uri=entity_uri,
        graph=graph,
        output_paths={
            "ttl": paths["ttl"],
            "xml": paths["xml"],
            "nt": paths["nt"],
            "jsonld": paths["jsonld"]
        }
    )


def copy_static(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)