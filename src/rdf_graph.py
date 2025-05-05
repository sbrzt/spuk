from rdflib import Graph, URIRef, RDF
from src.utils import get_uri_label, uri_to_filename, get_namespace
from collections import defaultdict
import pygal


class RDFGraph:
    def __init__(self, rdf_file: str):
        self.graph = Graph()
        self.graph.parse(rdf_file)
        self.entities = list(set(self.graph.subjects()))
        self.classes = self.get_classes()
        print(f"🔗 Loaded {len(self.graph)} triples from {rdf_file}")

    def get_entities(self):
        """Return all unique subjects in the RDF graph."""
        return self.entities

    def get_properties(self, subject):
        """Return all (predicate, object) pairs for a given subject."""
        results = []
        for p, o in self.graph.predicate_objects(subject):
            if isinstance(o, URIRef) and o in self.entities:
                results.append({
                    "predicate": get_uri_label(str(p)),
                    "predicate_uri": str(p),
                    "object": get_uri_label(str(o)),
                    "object_uri": uri_to_filename(str(o))
                })
            else:
                results.append({
                    "predicate": get_uri_label(str(p)),
                    "predicate_uri": str(p),
                    "object": get_uri_label(str(o)) if isinstance(o, URIRef) else str(o),
                    "object_uri": str(o) if isinstance(o, URIRef) else None
                })
        return results

    def get_classes(self):
        classes = set()
        for s, p, o in self.graph:
            if p == RDF.type and isinstance(o, URIRef):
                classes.add(str(o))
        return classes

    def get_class_entities(self):
        class_entities = {}
        for s, p, o in self.graph:
            if p == RDF.type and isinstance(o, URIRef):
                class_uri = str(o)
                if class_uri not in class_entities:
                    class_entities[class_uri] = {
                        "uri": class_uri,
                        "label": get_uri_label(class_uri),
                        "entities": [],
                        "frequency": 0
                    }
                class_entities[class_uri]["entities"].append(str(s))
                class_entities[class_uri]["frequency"] += 1
        return sorted(class_entities.values(), key=lambda x: x["frequency"], reverse=True)

    def get_property_usage(self):
        property_usage = defaultdict(int)
        for s, p, o in self.graph:
            if isinstance(p, URIRef):
                property_usage[str(p)] += 1
        prop_usage = []
        for uri, freq in property_usage.items():
            prop_label = get_uri_label(uri)
            prop_usage.append({
                "uri": uri,
                "label": prop_label,
                "frequency": freq
            })
        prop_usage = sorted(prop_usage, key=lambda x: x["frequency"], reverse=True)
        return prop_usage

    def generate_bar(self, title, data):
        bar_chart = pygal.HorizontalBar(
            style=pygal.style.Style(
                background="white",
                plot_background="white",
                opacity=".6",
                opacity_hover=".8",
                value_colors=("black",)
            ))
        bar_chart.title = title
        max_value = 0
        for d in data:
            bar_chart.add(d["label"], d["frequency"])
            if d["frequency"] > max_value:
                max_value = d["frequency"]
        bar_chart.y_labels = list(range(0, max_value + 1))
        return bar_chart.render(
            legend_at_bottom=True,
            legend_box_size=10,
            legend_at_bottom_columns=3,
            print_values=True,
            print_values_position="top",
            ).decode("utf-8")

    def get_summary(self):
        used_namespaces = set()
        for s, p, o in self.graph:
            if isinstance(s, URIRef):
                used_namespaces.add(get_namespace(s))
            used_namespaces.add(get_namespace(p))
            if isinstance(o, URIRef):
                used_namespaces.add(get_namespace(o))

        prefix_map = {str(ns): prefix for prefix, ns in self.graph.namespaces()}
        models_used = [
            (prefix_map[ns], ns) for ns in sorted(used_namespaces) if ns in prefix_map
        ]

        return {
            "num_triples": len(self.graph),
            "num_entities": len(self.entities),
            "num_classes": len(self.classes),
            "models_used": models_used,
            "class_entities_counts_chart": self.generate_bar("Entity frequency", self.get_class_entities()),
            "property_usage_chart": self.generate_bar("Property frequency", self.get_property_usage()),

        }
