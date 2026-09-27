# src/filesystem.py

import os
import json
import shutil
from pathlib import Path
from rdflib import URIRef, Graph
from typing import List
from src.path_resolver import get_entity_output_files
from src.html_renderer import HTMLRenderer
from src.rdf_serializer import RDFSerializer
from src.entity_model import Entity
from src.settings import GRAPH_SOURCE


def clean_output_dir(output_dir: Path) -> None:
    if output_dir.exists():
        for item in output_dir.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
    else:
        output_dir.mkdir(parents=True, exist_ok=True)


def entity_output_files_exist(uri: URIRef, output_dir: Path) -> bool:
    paths = get_entity_output_files(uri, output_dir)
    return all(paths[key].exists() for key in ("html", "ttl", "xml", "nt", "jsonld"))


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
    write_html_file(renderer.render_entities(), output_dir / "entities.html")
    type_ids = {}
    rows = []
    for entity in entities:
        type_idx = [type_ids.setdefault(t, len(type_ids)) for t in entity.types]
        rows.append([
            str(entity.uri),
            f"{entity.render_path}.html",
            type_idx,
            entity.subject_triple_count,
            entity.object_triple_count,
        ])
    index = {"types": list(type_ids), "rows": rows}
    (output_dir / "entities.json").write_text(
        json.dumps(index, separators=(",", ":"), ensure_ascii=False), encoding="utf-8"
    )


def write_entity_html(entity, output_dir: Path, renderer: HTMLRenderer) -> None:
    paths = get_entity_output_files(entity.uri, output_dir)
    html_content = renderer.render_entity(entity)
    write_html_file(html_content, paths["html"])


def write_entity_rdf(entity_uri: URIRef, output_dir: Path, graph: Graph, serializer: RDFSerializer, subgraph: Graph = None) -> None:
    paths = get_entity_output_files(entity_uri, output_dir)
    serializer.serialize_entity(
        entity_uri=entity_uri,
        graph=graph,
        output_paths={
            "ttl": paths["ttl"],
            "xml": paths["xml"],
            "nt": paths["nt"],
            "jsonld": paths["jsonld"]
        },
        subgraph=subgraph
    )


RESERVED_PAGES = {"index", "query", "entities"}


def doc_title(md_file: Path) -> str:
    return md_file.stem.replace("_", " ").capitalize()


def list_doc_files(markdown_dir: Path) -> List[Path]:
    if not markdown_dir.exists():
        return []
    files = []
    for md_file in sorted(markdown_dir.glob("*.md")):
        if md_file.stem in RESERVED_PAGES:
            print(f"Skipping doc '{md_file.name}': name clashes with a core page.")
            continue
        files.append(md_file)
    return files


def write_documentation_html(markdown_dir: Path, output_dir: Path, renderer: HTMLRenderer) -> None:
    for md_file in list_doc_files(markdown_dir):
        html_output_path = output_dir / f"{md_file.stem}.html"
        markdown_text = md_file.read_text(encoding="utf-8")
        content = renderer.render_documentation_page(title=doc_title(md_file), markdown_text=markdown_text)
        write_html_file(content, html_output_path)


def _copy_file_if_changed(src_path: str, dst_path: str) -> bool:
    if os.path.exists(dst_path):
        src_stat = os.stat(src_path)
        dst_stat = os.stat(dst_path)
        if src_stat.st_size == dst_stat.st_size and src_stat.st_mtime <= dst_stat.st_mtime:
            return False
    shutil.copy2(src_path, dst_path)
    return True


def copy_static(src_dir, dst_dir):
    os.makedirs(dst_dir, exist_ok=True)
    copied = 0
    total = 0
    for item in os.listdir(src_dir):
        if item == "data" and GRAPH_SOURCE.get("type") != "file":
            continue
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)
        if os.path.isdir(src_path):
            os.makedirs(dst_path, exist_ok=True)
            for root, _dirs, files in os.walk(src_path):
                rel = os.path.relpath(root, src_path)
                dst_root = os.path.join(dst_path, rel) if rel != "." else dst_path
                os.makedirs(dst_root, exist_ok=True)
                for name in files:
                    total += 1
                    if _copy_file_if_changed(os.path.join(root, name), os.path.join(dst_root, name)):
                        copied += 1
        else:
            total += 1
            if _copy_file_if_changed(src_path, dst_path):
                copied += 1
    print(f"Static files: {copied} copied, {total - copied} unchanged.")