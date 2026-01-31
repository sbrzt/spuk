# src/builder.py

from config import (
    GRAPH_SOURCE,
    OUTPUT_DIR,
    TEMPLATES_DIR,
    STATIC_DIR,
    ENABLE_CUSTOM_STATS,
    DOCUMENTATION_DIR
)
from src.graph_loader import load_graph
from src.entity_model import get_entities
from src.html_renderer import HTMLRenderer
from src.rdf_serializer import RDFSerializer
from src.stats_collector import collect_graph_stats
from src.custom_stats.engine import load_custom_stats
from src.filesystem import (
    ensure_entity_folder_exists, write_index_html, write_entities_html,
    write_entity_html, write_entity_rdf, write_query_html,
    copy_static, clean_output_dir, write_documentation_html
)
from tqdm import tqdm


class SiteBuilder:
    def __init__(self):
        self.graph = None
        self.stats = None
        self.custom_stats = {}
        self.renderer = None
        self.serializer = None
        self.entities = []
    
    def load_data(self):
        self.graph = load_graph(GRAPH_SOURCE)
        self.stats = collect_graph_stats(self.graph)
        if ENABLE_CUSTOM_STATS:
            self.custom_stats = load_custom_stats(self.graph)
        self.entities = list(get_entities(self.graph))
        docs_pages = []
        if DOCUMENTATION_DIR.exists():
            for md_file in DOCUMENTATION_DIR.glob("*.md"):
                docs_pages.append({
                    "title": md_file.stem.replace("_", " ").capitalize(),
                    "href": f"{md_file.stem}.html"
                })
        self.renderer = HTMLRenderer(TEMPLATES_DIR, OUTPUT_DIR, docs_pages)
        self.serializer = RDFSerializer()
        print(f"Data loaded: {len(self.graph)} triples, {len(self.entities)} entities.")

    def build_static(self):
        print("Updating static files...")
        copy_static(STATIC_DIR, OUTPUT_DIR)

    def build_content(self, limit=None):
        print("Rendering content...")
        if not limit:
            clean_output_dir(OUTPUT_DIR)
        write_index_html(OUTPUT_DIR, self.renderer, self.stats, self.custom_stats)
        write_query_html(OUTPUT_DIR, self.renderer)
        write_documentation_html(DOCUMENTATION_DIR, OUTPUT_DIR, self.renderer)
        target_entities = self.entities[:limit] if limit else self.entities
        for entity in target_entities:
            ensure_entity_folder_exists(entity.uri, OUTPUT_DIR)
            write_entity_html(entity, OUTPUT_DIR, self.renderer)
            if not limit:
                write_entity_rdf(entity.uri, OUTPUT_DIR, self.graph, self.serializer)
        if limit:
            write_entities_html(target_entities, OUTPUT_DIR, self.renderer)
        else:
            write_entities_html(self.entities, OUTPUT_DIR, self.renderer)
            copy_static(STATIC_DIR, OUTPUT_DIR)
    
    def run_full_build(self):
        self.load_data()
        self.build_content()