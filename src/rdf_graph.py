from rdflib import Graph, URIRef, RDF, Literal
from src.utils import get_uri_label, uri_to_filename, get_namespace
from collections import defaultdict
from SPARQLWrapper import SPARQLWrapper, GET, TURTLE
import pygal, logging, requests


class RDFGraph:
    def __init__(self, source: str, is_sparql_endpoint=False):
        self.graph = Graph()
        self.source = source
        if is_sparql_endpoint:
            self.load_from_sparql(source)
        else:
            self.graph.parse(source)
        self.entity_data = set()
        self.class_data = defaultdict(lambda: {
            "uri": None,
            "label": None,
            "entities": []
        })
        self.property_data = defaultdict(lambda: {
            "uri": None,
            "label": None,
            "type": None,
            "frequency": 0
        })
        self.property_object_data = defaultdict(list)
        self.model_data = defaultdict(lambda: {
            "uri": None,
            "label": None,
            "frequency": 0
        })
        self.in_degree = defaultdict(int)
        self.out_degree = defaultdict(int)
        self.analyze_graph()
        print(f"🔗 Loaded {len(self.graph)} triples from {source}")


    def load_from_sparql(self, endpoint_url: str):
        query = """
        CONSTRUCT { ?s ?p ?o }
        WHERE { ?s ?p ?o }
        """
        sparql = SPARQLWrapper(endpoint_url)
        sparql.setQuery(query)
        sparql.setMethod(GET)
        sparql.setReturnFormat(TURTLE)
        response = sparql.query().convert()
        self.graph.parse(data=response.decode("utf-8"), format="turtle")
        print(f"✅ Data loaded from {endpoint_url}.")

    def get_entity_data(self):
        return self.entity_data

    def get_class_data(self):
        return sorted(
            self.class_data.values(),
            key=lambda x: x["frequency"],
            reverse=True
        )

    def get_property_data(self):
        return sorted(
            self.property_data.values(),
            key=lambda x: x["frequency"],
            reverse=True
        )
    
    def get_property_object_data(self):
        return dict(self.property_object_data)

    def get_model_data(self):
        return sorted(
            self.model_data.values(),
            key=lambda x: x["frequency"],
            reverse=True
        )

    def analyze_graph(self):
        self.entity_data.update([str(s) for s in self.graph.subjects()])
        for s, p, o in self.graph:
            s_str = str(s)
            self.out_degree[str(s)] += 1
            if isinstance(s, URIRef):
                for prefix, ns in self.graph.namespaces():
                    if get_namespace(s) == str(ns):
                        model_uri = get_namespace(s)
                        self.model_data[model_uri]["uri"] = model_uri
                        self.model_data[model_uri]["label"] = prefix
                        self.model_data[model_uri]["frequency"] += 1
                
            if isinstance(p, URIRef):
                property_uri = str(p)
                property_label = get_uri_label(property_uri)
                object_label, object_uri = self.format_object(o)
                self.property_object_data[s_str].append({
                    "property_label": property_label,
                    "property_uri": property_uri,
                    "object_label": object_label,
                    "object_uri": object_uri,
                    "is_type": True if p == RDF.type else False
                })
                self.property_data[property_uri]["label"] = property_label
                self.property_data[property_uri]["uri"] = property_uri
                self.property_data[property_uri]["frequency"] += 1
                for prefix, ns in self.graph.namespaces():
                    if get_namespace(p) == str(ns):
                        model_uri = get_namespace(p)
                        self.model_data[model_uri]["uri"] = model_uri
                        self.model_data[model_uri]["label"] = prefix
                        self.model_data[model_uri]["frequency"] += 1
            
            if isinstance(o, URIRef):
                self.in_degree[str(o)] += 1
                self.property_data[property_uri]["type"] = "object"
                if p == RDF.type:
                    class_uri = str(o)
                    self.class_data[class_uri]["label"] = get_uri_label(class_uri)
                    self.class_data[class_uri]["uri"] = class_uri
                    self.class_data[class_uri]["entities"].append(s_str)
            elif isinstance(o, Literal):
                self.property_data[property_uri]["type"] = "data"
            for prefix, ns in self.graph.namespaces():
                if get_namespace(o) == str(ns):
                    model_uri = get_namespace(o)
                    self.model_data[model_uri]["uri"] = model_uri
                    self.model_data[model_uri]["label"] = prefix
                    self.model_data[model_uri]["frequency"] += 1

        self.entity_data = list(self.entity_data)

        for data in self.class_data.values():
            data["frequency"] = len(data["entities"])

    def format_object(self, o):
        if isinstance(o, URIRef):
            o_str = str(o)
            if o_str in self.entity_data:
                return get_uri_label(o_str), uri_to_filename(o_str)
            return get_uri_label(o_str), o_str
        return str(o), None

    def get_property_ratio(self):
        object_property_total = sum(
            prop["frequency"] for prop in self.property_data.values() if prop["type"] == "object"
        )
        data_property_total = sum(
            prop["frequency"] for prop in self.property_data.values() if prop["type"] == "data"
        )

        if data_property_total > 0:
            ratio = object_property_total / data_property_total
        else:
            ratio = float('inf')
        return round(ratio, 2)


    def generate_bar(self, title, data):
        bar_chart = pygal.HorizontalBar(
            style=pygal.style.Style(
                background="white",
                plot_background="white",
                opacity=".6",
                opacity_hover=".8",
                value_colors=("black",)
            )
        )
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
        return {
            "source": self.source,
            "num_triples": len(self.graph),
            "num_entities": len(self.get_entity_data()),
            "num_properties": len(self.get_property_data()),
            "num_classes": len(self.get_class_data()),
            "avg_degree": round(sum({e: self.in_degree[e] + self.out_degree[e] for e in self.get_entity_data()}.values()) / len(self.get_entity_data()), 2),
            "property_ratio": self.get_property_ratio(),
            "models_used": self.get_model_data(),
            "class_entities_counts_chart": self.generate_bar("Entity frequency", self.get_class_data()),
            "property_usage_chart": self.generate_bar("Property frequency", self.get_property_data()),
            "models_usage": self.generate_bar("Model usage", self.get_model_data())
        }
