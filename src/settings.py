# src/settings.py
#
# Loads config.toml at the project root and exposes it as module-level
# constants. Edit config.toml, not this file, to change settings.

import tomllib
from pathlib import Path

_CONFIG_PATH = Path(__file__).parent.parent / "config.toml"

with open(_CONFIG_PATH, "rb") as _f:
    _cfg = tomllib.load(_f)

# --- Graph source configuration ---
_graph_source = _cfg["graph_source"]
GRAPH_SOURCE = {
    "type": _graph_source["type"],
    "file_path": Path(_graph_source["file_path"]),
    "file_format": _graph_source["file_format"],
    "sparql_endpoint": _graph_source["sparql_endpoint"],
}

# --- Output configuration ---
_output = _cfg["output"]
OUTPUT_DIR = Path(_output["output_dir"])
TEMPLATES_DIR = Path(_output["templates_dir"])
STATIC_DIR = Path(_output["static_dir"])
DOCUMENTATION_DIR = Path(_output["documentation_dir"])

# --- Modelling configuration ---
TYPE_PROPERTY = _cfg["modelling"]["type_property"]
LABEL_PATH = _cfg["modelling"].get("label_path", [])

# --- Overview page configuration ---
INDEX_CARDS = _cfg["index"]["cards"]
INDEX_CHARTS = _cfg["index"]["charts"]

# --- SPARQL queries configuration ---
PREDEFINED_QUERIES = _cfg["predefined_queries"]

# --- Data visualization configuration ---
N_OBJECTS = _cfg["data_viz"]["n_objects"]

# --- Entity graph configuration ---
GRAPH_VIS_OPTIONS = _cfg["graph_vis_options"]

# --- Theme configuration ---
THEME = {
    "colors": _cfg["theme"]["colors"],
    "hero": _cfg["theme"]["hero"],
}
