# src/html_renderer.py

import os
import json
import colorsys
import hashlib
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path, PurePosixPath
from rdflib import URIRef, Literal, RDF
from rdflib.graph import Graph
from typing import List, Dict, Any
from src.entity_model import Entity
from urllib.parse import urlparse
from src.settings import (
    GRAPH_VIS_OPTIONS,
    GRAPH_SOURCE,
    PREDEFINED_QUERIES,
    STATIC_DIR,
    THEME
)


class HTMLRenderer:

    def __init__(self, templates_path: Path, site_root: Path, docs_pages: List[Dict[str, str]] = None):
        self.env = Environment(
            loader=FileSystemLoader(str(templates_path)),
            autoescape=select_autoescape(["html"]),
            auto_reload=True
        )
        self.env.globals["theme"] = THEME
        self.env.globals["theme_hsl"] = {
            name: self._hex_to_hsl(value) for name, value in THEME["colors"].items()
        }
        self.env.globals["asset_version"] = self._compute_asset_version()
        self.site_root = site_root.resolve()
        self.docs_pages = docs_pages or []

    @staticmethod
    def _hex_to_hsl(hex_color: str) -> Dict[str, str]:
        hex_color = hex_color.lstrip("#")
        r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (0, 2, 4))
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        return {"h": f"{h * 360:.0f}deg", "s": f"{s * 100:.0f}%", "l": f"{l * 100:.0f}%"}

    @staticmethod
    def _compute_asset_version() -> str:
        digest = hashlib.sha1()
        for path in sorted([*STATIC_DIR.glob("css/*"), *STATIC_DIR.glob("js/*")]):
            digest.update(path.read_bytes())
        return digest.hexdigest()[:10]

    def render_index(self, cards, charts) -> str:
        return self.env.get_template("index.html").render(
            title="Index",
            cards=cards,
            charts=charts,
            base_url="",
            docs_pages=self.docs_pages
        )
    
    def render_query(self) -> str:
        is_endpoint = GRAPH_SOURCE["type"] == "sparql"
        data_source = (
            GRAPH_SOURCE["sparql_endpoint"] if is_endpoint
            else str(Path(GRAPH_SOURCE["file_path"]).relative_to(STATIC_DIR))
        )
        return self.env.get_template("query.html").render(
            title="Query Interface",
            data_source=data_source,
            data_source_is_endpoint=is_endpoint,
            queries=PREDEFINED_QUERIES,
            base_url="",
            docs_pages=self.docs_pages
        )

    def render_entity(self, entity: Entity) -> str:
        related_uris = set(entity.get_related_entities())
        current_path = self.site_root / entity.render_path
        base_url = self._compute_base_url(entity.render_path)
        graph_data = self._get_entity_graph_data(entity.get_entity_subgraph())
        return self.env.get_template("entity.html").render(
            title=f"{entity.uri}",
            entity=entity,
            filename=self._compute_internal_value(entity.uri),
            property_object_pairs=self._format_entity_triples(
                pairs=entity.get_predicates_objects(),
                related_uris=related_uris,
                direction="out",
                current_path=current_path
            ),
            subject_property_pairs=self._format_entity_triples(
                pairs=entity.get_subjects_predicates(),
                related_uris=related_uris,
                direction="in",
                current_path=current_path
            ),
            path=entity.render_path,
            base_url=base_url,
            docs_pages=self.docs_pages,
            graph_data=graph_data,
            graph_options=GRAPH_VIS_OPTIONS
        )

    def render_entities(self) -> str:
        return self.env.get_template("entities.html").render(
            title="Entities",
            base_url="",
            docs_pages=self.docs_pages
        )

    def render_documentation_page(self, title: str, markdown_text: str, base_url: str = "") -> str:
        html_content = markdown.markdown(markdown_text, extensions=["fenced_code", "tables"])
        template = self.env.get_template("documentation.html")
        return template.render(
            title=title, 
            content=html_content, 
            base_url=base_url,
            docs_pages=self.docs_pages
        )

    
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


    def _format_entity_triples(self, pairs, related_uris, direction="out", current_path=""):
        formatted = []
        current_dir = current_path.parent
        for a, b in pairs:
            if str(a if direction == "out" else b) == str(RDF.type):
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
        uri = str(uri)
        if "#" in uri:
            return uri.split("#")[-1]
        elif "/" in uri:
            return uri.split("/")[-1]
        return uri