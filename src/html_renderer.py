# src/html_renderer.py

import os
import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path, PurePosixPath
from rdflib import URIRef, Literal
from rdflib.graph import Graph
from typing import List, Dict, Any
from src.stats_collector import GraphStats
from src.entity_model import Entity
from urllib.parse import urlparse
from config import (
    GRAPH_VIS_OPTIONS,
    GRAPH_SOURCE,
    PREDEFINED_QUERIES
)


class HTMLRenderer:
    
    def __init__(self, templates_path: Path, site_root: Path):
        self.env = Environment(loader=FileSystemLoader(str(templates_path)))
        self.index_template = self.env.get_template("index.html")
        self.query_template = self.env.get_template("query.html")
        self.entity_template = self.env.get_template("entity.html")
        self.entities_template = self.env.get_template("entities.html")
        self.site_root = site_root.resolve()

    def render_index(self, stats: GraphStats, custom_stats=None) -> str:
        return self.index_template.render(
            stats=stats, 
            custom_stats=custom_stats or {},
            base_url=""
        )
    
    def render_query(self) -> str:
        return self.query_template.render(
            data_source=GRAPH_SOURCE["sparql_endpoint"] if GRAPH_SOURCE["type"] == "sparql" else GRAPH_SOURCE["file_path"],
            queries=PREDEFINED_QUERIES,
            base_url=""
        )

    def render_entity(self, entity: Entity) -> str:
        related_uris = set(entity.get_related_entities())
        current_path = self.site_root / entity.render_path
        base_url = self._compute_base_url(entity.render_path)
        graph_data = self._get_entity_graph_data(self, entity.get_entity_subgraph())
        return self.entity_template.render(
            entity=entity,
            filename=self._compute_internal_value(entity.uri),
            property_object_pairs=self._format_entity_triples(
                self=self,
                pairs=entity.get_predicates_objects(),
                related_uris=related_uris,
                direction="out",
                current_path=current_path
            ),
            subject_property_pairs=self._format_entity_triples(
                self=self,
                pairs=entity.get_subjects_predicates(),
                related_uris=related_uris,
                direction="in",
                current_path=current_path
            ),
            path=entity.render_path,
            base_url=base_url,
            graph_data=json.dumps(graph_data),
            graph_options=json.dumps(GRAPH_VIS_OPTIONS)
        )

    def render_entities(self, entities: List[Entity]) -> str:
        return self.entities_template.render(
            entities=entities,
            base_url=""
        )

    
    @staticmethod
    def _get_entity_graph_data(self, graph: Graph) -> Dict[str, Any]:
        nodes = {}
        edges = []
        for s, p, o in graph:
            for node in [s, o]:
                node_id = str(node)
                if isinstance(node, URIRef) and node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": self._compute_internal_value(node_id),
                        "title": node_id,
                        "shape": "ellipse"
                    }
                elif isinstance(node, Literal) and node_id not in nodes:
                    nodes[node_id] = {
                        "id": node_id,
                        "label": node_id,
                        "title": node_id,
                        "shape": "box",
                        "color": "#DDEEFF"
                    }
            edges.append({
                "from": str(s),
                "to": str(o),
                "label": self._compute_internal_value(p),
                "arrows": "to"
            })
        return {
            "nodes": list(nodes.values()),
            "edges": edges
        }


    @staticmethod
    def _format_entity_triples(self, pairs, related_uris, direction="out", current_path=""):
        formatted = []
        current_dir = current_path.parent
        for a, b in pairs:
            if str(a if direction == "out" else b) == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
                continue
            uri = b if direction == "out" else a
            is_uri = isinstance(uri, URIRef)
            uri_str = str(uri)
            is_internal = is_uri and uri in related_uris
            target_file_path = ""
            if is_internal:
                parsed = urlparse(uri_str)
                path_parts = parsed.path.strip("/").split("/")
                if path_parts:
                    target_file_path = self.site_root / Path(*path_parts) / f"{path_parts[-1]}"
                    target_file_path = os.path.relpath(target_file_path, start=current_dir)
            formatted.append({
                "property_uri": str(a if direction == "out" else b),
                "property_label": self._compute_internal_value(str(a if direction == "out" else b)),
                "value": uri_str,
                "is_literal": not is_uri,
                "is_internal": is_internal,
                "internal_href": target_file_path,
            })
        return formatted

    @staticmethod
    def _compute_base_url(path: str) -> str:
        if path in ("index.html", "entities.html"):
            return ""
        depth = PurePosixPath(path).parent.parts
        return "../" * len(depth)

    @staticmethod
    def _compute_internal_value(uri: str) -> str:
        if "#" in uri:
            return uri.split("#")[-1]
        elif "/" in uri:
            return uri.split("/")[-1]