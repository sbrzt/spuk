# config.py

from pathlib import Path


# --- Graph source configuration ---
TEST_GRAPH_SOURCE = "static/data/merged_graph_output.ttl"
GRAPH_SOURCE = {
    "type": "file",                                                     # sparql | file
    "file_path": Path(TEST_GRAPH_SOURCE),
    "file_format": "turtle",
    "sparql_endpoint": "https://w3id.org/dharc/sparql/chad-kg"
}

# --- Output configuration ---
OUTPUT_DIR = Path("docs/")
TEMPLATES_DIR = "templates"
STATIC_DIR = "static"
DOCUMENTATION_DIR = Path("doc")

# --- Modelling configuration
TYPE_PROPERTY = "http://www.cidoc-crm.org/cidoc-crm/P2_has_type"

# --- Custom stats configuration ---
ENABLE_CUSTOM_STATS = False
STATS_CONFIG = "src/custom_stats/config.yaml"

# --- SPARQL queries configuration ---
PREDEFINED_QUERIES = [
    {
        "name": "All classes",
        "query": "SELECT DISTINCT ?class WHERE { ?s a ?class } LIMIT 100"
    },
    {
        "name": "All properties",
        "query": "SELECT DISTINCT ?property WHERE { ?s ?property ?o } LIMIT 100"
    }
]

# --- Data visualization configuration
N_OBJECTS = 5

# --- Entity graph configuration ---
GRAPH_VIS_OPTIONS = {
    "layout": {
        "improvedLayout": True
    },
    "physics": {
        "enabled": True,
        "solver": "repulsion",
        "repulsion": {
            "nodeDistance": 200,
            "springLength": 200,
            "springConstant": 0.03,
            "damping": 0.09
        },
        "stabilization": {
            "enabled": True,
            "iterations": 250,
            "fit": True
        }
    },
    "nodes": {
        "shape": "dot",
        "size": 12,
        "font": { "size": 14 }
    },
    "edges": {
        "arrows": "to",
        "font": { "align": "middle", "size": 12 }
    }
}

