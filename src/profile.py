from src.knowledge_graph import KnowledgeGraph
from src.models import EntityData, PropertyValuePair
from src.utils import get_uri_label
from typing import List, Dict, Optional
from rdflib import URIRef, RDF, Literal


class Profile:

    def __init__(
        self,
        knowledge_graph: KnowledgeGraph
        ) -> None:

        self._kg = knowledge_graph
        self.graph = self._kg.get_graph()
        self.entities: Dict[str, EntityData] = {}
        
        self.object_properties: set[str] = set()
        self.data_properties: set[str] = set()

        self._analyze()


    def _analyze(
        self
        ) -> None:

        for s, p, o in self.graph:
            s_str = str(s)
            if s_str not in self.entities:
                self.entities[s_str] = EntityData(
                    uri = s_str,
                    types = [],
                    properties = []
                )
            p_str = str(p)
            o_str = str(o)

            if isinstance(p, URIRef):
                p_label = get_uri_label(p_str)
                is_literal = isinstance(o, Literal)

                if p == RDF.type:
                    class_uri = str(o)
                    self.entities[s_str].types.append(class_uri)
                    # CLASS COUNTS HERE
                    continue
                else:
                    if is_literal:
                        self.data_properties.add(p_str)
                    else:
                        self.object_properties.add(p_str)

                self.entities[s_str].properties.append(
                    PropertyValuePair(
                        property_label = p_label,
                        property_uri = p_str,
                        value = o_str,
                        is_literal = is_literal
                    )
                )

    @property
    def num_triples(
        self
        ) -> int:
        return len(self.graph)

    @property
    def num_entities(
        self
        ) -> int:
        return len(self.entities)

    @property
    def num_object_properties(
        self
        ) -> int:
        return len(self.object_properties)
    
    @property
    def num_data_properties(
        self
        ) -> int:
        return len(self.data_properties)
    
    
    def get_summary(
        self
        ) -> dict:
        return {
            "num_triples": self.num_triples,
            "num_entities": self.num_entities,
            "num_object_properties": self.num_object_properties,
            "num_data_properties": self.num_data_properties
        }

    '''
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

    def get_most_connected(self):
        most_connected = None
        max_length = 0
        for key, value in self.get_property_object_data().items():
            if isinstance(value, list):
                if len(value) > max_length:
                    most_connected = key
                    max_length = len(value)
        return generate_path(most_connected)

    def add_model_data(self, el):
        for prefix, ns in self.graph.namespaces():
            if get_namespace(el) == str(ns):
                model_uri = get_namespace(el)
                self.model_data[model_uri]["uri"] = model_uri
                self.model_data[model_uri]["label"] = prefix
                self.model_data[model_uri]["frequency"] += 1


    def analyze_graph(self):
        self.entity_data.update([str(s) for s in self.graph.subjects()])
        for s, p, o in self.graph:
            s_str = str(s)
            self.out_degree[str(s)] += 1
            if isinstance(s, URIRef):
                self.add_model_data(s)
                
            if isinstance(p, URIRef):
                if p != RDF.type:
                    property_uri = str(p)
                    property_label = get_uri_label(property_uri)
                    object_label, object_uri = self.format_object(o)
                    self.property_object_data[s_str].append({
                        "property_label": property_label,
                        "property_uri": property_uri,
                        "object_label": object_label,
                        "object_uri": object_uri,
                    })
                    self.property_data[property_uri]["label"] = property_label
                    self.property_data[property_uri]["uri"] = property_uri
                    self.property_data[property_uri]["frequency"] += 1
                    self.add_model_data(p)
            
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
            self.add_model_data(o)

        self.entity_data = list(self.entity_data)

        for data in self.class_data.values():
            data["frequency"] = len(data["entities"])

    def format_object(self, o):
        o_str = str(o)
        if isinstance(o, URIRef):
            if o_str in self.entity_data:
                return o_str, f"{remove_root(generate_path(o_str))}/{uri_to_filename(o_str)}"
            return o_str, o_str
        return o_str, None

    def get_summary(self):
        return {
            "source": self.source,
            "num_triples": len(self.graph),
            "num_entities": len(self.get_entity_data()),
            "num_properties": len(self.get_property_data()),
            "num_classes": len(self.get_class_data()),
            "avg_degree": round(sum({e: self.in_degree[e] + self.out_degree[e] for e in self.get_entity_data()}.values()) / len(self.get_entity_data()), 2),
            "property_ratio": self.get_property_ratio(),
            "most_connected": self.get_most_connected(),
            "models_used": self.get_model_data(),
        }
    '''