# src/builder.py

import multiprocessing
import shutil
from src.settings import (
    GRAPH_SOURCE,
    OUTPUT_DIR,
    TEMPLATES_DIR,
    STATIC_DIR,
    DOCUMENTATION_DIR,
    INDEX_CARDS,
    INDEX_CHARTS
)
from rdflib import URIRef
from src.path_resolver import get_entity_output_files
from src.graph_loader import load_graph
from src.entity_model import get_entities
from src.html_renderer import HTMLRenderer
from src.rdf_serializer import RDFSerializer
from src.stats_collector import collect_graph_stats, build_index_cards, build_index_charts
from src.filesystem import (
    ensure_entity_folder_exists, write_index_html, write_entities_html,
    write_entity_html, write_entity_rdf, write_query_html,
    copy_static, clean_output_dir, write_documentation_html,
    list_doc_files, doc_title, entity_output_files_exist
)
from src.manifest import hash_templates, hash_entity, load_manifest, save_manifest
from tqdm import tqdm


_worker_builder = None


def _write_entity(index):
    builder = _worker_builder
    entity = builder.entities[index]
    new_hash = hash_entity(entity, builder.template_hash)
    uri = str(entity.uri)
    unchanged = (
        builder.old_manifest.get(uri) == new_hash
        and entity_output_files_exist(entity.uri, OUTPUT_DIR)
    )
    if not unchanged:
        builder._write_entity(entity)
    return uri, new_hash


class SiteBuilder:
    def __init__(self):
        self.graph = None
        self.stats = None
        self.index_cards = []
        self.index_charts = []
        self.renderer = None
        self.serializer = None
        self.entities = []
        self.template_hash = ""
        self.old_manifest = {}

    def load_data(self):
        print("Loading graph...")
        self.graph = load_graph(GRAPH_SOURCE)
        print("Computing stats...")
        self.stats = collect_graph_stats(self.graph)
        self.index_cards = build_index_cards(self.stats, INDEX_CARDS)
        self.index_charts = build_index_charts(self.graph, self.stats, INDEX_CHARTS)
        print("Indexing entities...")
        self.entities = list(get_entities(self.graph))
        self._check_path_collisions()
        docs_pages = [
            {"title": doc_title(md_file), "href": f"{md_file.stem}.html"}
            for md_file in list_doc_files(DOCUMENTATION_DIR)
        ]
        self.renderer = HTMLRenderer(TEMPLATES_DIR, OUTPUT_DIR, docs_pages)
        self.serializer = RDFSerializer()
        print(f"Data loaded: {len(self.graph)} triples, {len(self.entities)} entities.")

    def _check_path_collisions(self):
        seen = {}
        for entity in self.entities:
            path = get_entity_output_files(entity.uri, OUTPUT_DIR)["dir"]
            if path in seen:
                raise ValueError(f"Output path collision: {seen[path]} and {entity.uri} both map to {path}")
            seen[path] = entity.uri

    def _write_entity(self, entity):
        ensure_entity_folder_exists(entity.uri, OUTPUT_DIR)
        write_entity_html(entity, OUTPUT_DIR, self.renderer)
        write_entity_rdf(entity.uri, OUTPUT_DIR, self.graph, self.serializer, entity.get_entity_subgraph())

    def _write_entities_parallel(self):
        global _worker_builder
        _worker_builder = self
        self.template_hash = hash_templates(TEMPLATES_DIR)
        self.old_manifest = load_manifest(OUTPUT_DIR)
        new_manifest = {}
        skipped = 0
        context = multiprocessing.get_context("fork")
        with context.Pool() as pool:
            results = pool.imap_unordered(_write_entity, range(len(self.entities)), chunksize=200)
            for uri, new_hash in tqdm(results, total=len(self.entities), desc="Entities", unit="entity"):
                new_manifest[uri] = new_hash
                if self.old_manifest.get(uri) == new_hash:
                    skipped += 1
        orphaned = set(self.old_manifest) - set(new_manifest)
        for uri in orphaned:
            entity_dir = get_entity_output_files(URIRef(uri), OUTPUT_DIR)["dir"]
            if entity_dir.exists():
                shutil.rmtree(entity_dir)
        save_manifest(OUTPUT_DIR, new_manifest)
        print(f"Entities: {len(new_manifest) - skipped} rendered, {skipped} unchanged, {len(orphaned)} removed.")

    def build_static(self):
        print("Updating static files...")
        copy_static(STATIC_DIR, OUTPUT_DIR)

    def build_content(self, limit=None):
        print("Rendering content...")
        if not OUTPUT_DIR.exists():
            clean_output_dir(OUTPUT_DIR)
        write_index_html(OUTPUT_DIR, self.renderer, self.index_cards, self.index_charts)
        write_query_html(OUTPUT_DIR, self.renderer)
        write_documentation_html(DOCUMENTATION_DIR, OUTPUT_DIR, self.renderer)
        target_entities = self.entities[:limit] if limit else self.entities
        if limit:
            for entity in tqdm(target_entities, desc="Entities", unit="entity"):
                self._write_entity(entity)
        else:
            self._write_entities_parallel()
        if limit:
            write_entities_html(target_entities, OUTPUT_DIR, self.renderer)
        else:
            write_entities_html(self.entities, OUTPUT_DIR, self.renderer)
            copy_static(STATIC_DIR, OUTPUT_DIR)
    
    def run_full_build(self):
        self.load_data()
        self.build_content()