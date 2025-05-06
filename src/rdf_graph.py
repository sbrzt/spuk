from rdflib import Graph, URIRef, RDF
from src.utils import get_uri_label, uri_to_filename, get_namespace
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, GET, TURTLE
import pygal, logging, requests


class RDFGraph:
    def __init__(self, source: str, is_sparql_endpoint=False):
        self.graph = Graph()
        if is_sparql_endpoint:
            self.load_from_sparql(source)
        else:
            self.graph.parse(source)
        self.entities = list(set(self.graph.subjects()))
        self.classes = self.get_classes()
        print(f"🔗 Loaded {len(self.graph)} triples from {source}")

    def load_from_sparql(self, endpoint_url: str):
        query = """
        CONSTRUCT { ?s ?p ?o }
        WHERE { ?s ?p ?o }
        """
        sparql = SPARQLWrapper(endpoint_url, agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        sparql.setQuery(query)
        sparql.setMethod(GET)
        sparql.setReturnFormat(TURTLE)
        response = sparql.query().convert()
        self.graph.parse(data=response.decode("utf-8"), format="turtle")
        print(f"✅ Data loaded from {endpoint_url}.")

    def get_entities(self):
        """Return all entities in the RDF graph."""
        return self.entities

    def get_properties(self, subject):
        """Return all (predicate, object) pairs for a given subject."""
        def format_object(o):
            if isinstance(o, URIRef) and o in self.entities:
                return {
                    "is_data_property": False,
                    "is_internal": True,
                    "object_label": get_uri_label(str(o)),
                    "object_uri": uri_to_filename(str(o))
                }
            elif isinstance(o, URIRef) and o not in self.entities:
                return {
                    "is_data_property": False,
                    "is_internal": False,
                    "object_label": get_uri_label(str(o)),
                    "object_uri": str(o)
                }
            else:
                return {
                    "is_data_property": True,
                    "is_internal": False,
                    "object_label": str(o),
                    "object_uri": None
                }
        return [
            {
                "predicate_label": get_uri_label(str(p)),
                "predicate_uri": str(p),
                **format_object(o)
            }
            for p, o in self.graph.predicate_objects(subject)
        ]

    

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
        for d in data:
            bar_chart.add(d["label"], d["frequency"])
        return bar_chart.render(
            legend_at_bottom=True,
            legend_box_size=5,
            legend_at_bottom_columns=3,
            print_values=True,
            print_values_position="top",
            order_min=1,
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

    def load_from_sparql(self, endpoint_url: str):
        query = """
        CONSTRUCT { ?s ?p ?o }
        WHERE { ?s ?p ?o }
        """
        sparql = SPARQLWrapper(endpoint_url, agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11")
        sparql.setQuery(query)
        sparql.setMethod(GET)
        sparql.setReturnFormat(TURTLE)
        response = sparql.query().convert()
        self.graph.parse(data=response.decode("utf-8"), format="turtle")
        print("✅ Data loaded using SPARQLWrapper.")
