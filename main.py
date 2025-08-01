# main.py

from config import (
    GRAPH_SOURCE, 
    OUTPUT_DIR, 
    TEMPLATES_DIR, 
    STATIC_DIR,
    ENABLE_CUSTOM_STATS,
)
from tqdm import tqdm
from src.graph_loader import load_graph
from src.entity_model import get_entities
from src.html_renderer import HTMLRenderer
from src.rdf_serializer import RDFSerializer
from src.stats_collector import collect_graph_stats
from src.custom_stats.engine import load_custom_stats
from src.filesystem import (
    ensure_entity_folder_exists,
    write_index_html,
    write_entities_html,
    write_entity_html,
    write_entity_rdf,
    write_query_html,
    copy_static
)


def main():
    
    print("Loading RDF graph...")
    graph = load_graph(GRAPH_SOURCE)
    print(f"Loaded {len(graph)} triples.")

    print("Collecting graph statistics...")
    stats = collect_graph_stats(graph)
    custom_stats = {}
    if ENABLE_CUSTOM_STATS:
        custom_stats = load_custom_stats(graph)

    renderer = HTMLRenderer(templates_path=TEMPLATES_DIR, site_root=OUTPUT_DIR)
    serializer = RDFSerializer()
    
    print("Rendering entity pages...")
    entities = list(get_entities(graph))

    for entity in tqdm(entities):
        ensure_entity_folder_exists(entity.uri, OUTPUT_DIR)
        write_entity_html(entity, OUTPUT_DIR, renderer)
        write_entity_rdf(entity.uri, OUTPUT_DIR, graph, serializer)

    print("Rendering main pages...")
    write_index_html(OUTPUT_DIR, renderer, stats, custom_stats)
    write_entities_html(entities, OUTPUT_DIR, renderer)
    write_query_html(OUTPUT_DIR, renderer)

    print("Copying static files...")
    copy_static(STATIC_DIR, OUTPUT_DIR)

    print("All entities processed.")

if __name__ == "__main__":
    main()