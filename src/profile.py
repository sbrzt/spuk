from src.knowledge_graph import KnowledgeGraph
from src.models import EntityData, PropertyValuePair
from src.utils import get_uri_label, get_namespace
from typing import List, Dict, Optional, Tuple
from rdflib import URIRef, RDF, Literal
from collections import defaultdict


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
        self.property_frequencies: dict[str, int] = defaultdict(int)
        self.class_frequencies: dict[str, int] = defaultdict(int)
        self.model_frequencies: dict[Tuple[str, str], int] = defaultdict(int)

        self._analyze()


    def _analyze(
        self
        ) -> None:

        namespaces = dict(self.graph.namespaces())

        def get_model_key(
            uri: str
            ) -> Optional[Tuple[str, str]]:
            for prefix, ns in namespaces.items():
                if uri.startswith(str(ns)):
                    return (prefix, str(ns))
            return None

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

            model_key = get_model_key(p_str if p != RDF.type else o_str)
            if model_key:
                self.model_frequencies[model_key] += 1

            if isinstance(p, URIRef):
                p_label = get_uri_label(p_str)
                is_literal = isinstance(o, Literal)

                if p == RDF.type:
                    class_uri = str(o)
                    self.entities[s_str].types.append(class_uri)
                    self.class_frequencies[o_str] += 1
                    continue
                else:
                    self.property_frequencies[p_str] += 1
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
    def num_properties(
        self
        ) -> int:
        return sum(self.property_frequencies.values())

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

    @property
    def num_classes(
        self
        ) -> int:
        return len(self.class_frequencies)

    @property
    def num_models(
        self
        ) -> int:
        return len(self.model_frequencies)

    @property
    def most_frequent_properties(
        self,
        n: int = 10
        ) -> List[Tuple[str, int]]:
        return sorted(
            self.property_frequencies.items(),
            key = lambda x: x[1],
            reverse = True
        )[:n]

    @property
    def most_frequent_classes(
        self,
        n: int = 10
        ) -> List[Tuple[str, int]]:
        return sorted(
            self.class_frequencies.items(),
            key = lambda x: x[1],
            reverse = True
        )[:n]

    @property
    def most_frequent_models(
        self,
        n: int = 10
        ) -> List[Tuple[str, str, int]]:
        return [
            (prefix, ns, count)
            for (prefix, ns), count in sorted(
                self.model_frequencies.items(),
                key = lambda x: x[1],
                reverse = True
            )[:n]
        ]
    
    
    def get_summary(
        self
        ) -> dict:
        return {
            "num_triples": self.num_triples,
            "num_entities": self.num_entities,
            "num_properties": self.num_properties,
            "num_object_properties": self.num_object_properties,
            "num_data_properties": self.num_data_properties,
            "num_classes": self.num_classes,
            "num_models": self.num_models
        }

    '''
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

    "avg_degree": round(sum({e: self.in_degree[e] + self.out_degree[e] for e in self.get_entity_data()}.values()) / len(self.get_entity_data()), 2),
    "property_ratio": self.get_property_ratio(),
    "most_connected": self.get_most_connected(),
    '''