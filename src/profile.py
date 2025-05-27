from src.knowledge_graph import KnowledgeGraph
from src.models import EntityData, PropertyValuePair
from src.utils import get_uri_label, get_namespace
from typing import List, Dict, Optional, Tuple
from rdflib import URIRef, RDF, Literal
from collections import defaultdict


class Profile:
    """
    An analytical profile of a knowledge graph, providing descriptive statistics
    and structural summaries such as entity counts, property usage, class distribution,
    and ontology/model frequencies.

    Attributes:
        entities (Dict[str, EntityData]): Map of entity URIs to their associated data.
        object_properties (set[str]): Set of URIs used as object properties.
        data_properties (set[str]): Set of URIs used as data (literal) properties.
        property_frequencies (dict[str, int]): Frequency count of each property URI.
        class_frequencies (dict[str, int]): Frequency count of each class URI.
        model_frequencies (dict[Tuple[str, str], int]): Frequency of each namespace (prefix, URI) used in the graph.
    """

    def __init__(
        self,
        knowledge_graph: KnowledgeGraph
        ) -> None:
        """
        Initializes the Profile with a given KnowledgeGraph instance.

        Args:
            knowledge_graph (KnowledgeGraph): The RDF graph wrapper to be analyzed.
        """
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
        """
        Performs the core analysis of the RDF graph.
        Extracts and counts entities, classes, properties, and models used.
        """
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
        """
        Returns the total number of RDF triples in the graph.
        """
        return len(self.graph)

    @property
    def num_entities(
        self
        ) -> int:
        """
        Returns the number of unique entities (subjects) in the graph.
        """
        return len(self.entities)

    @property
    def num_properties(
        self
        ) -> int:
        """
        Returns the total number of property usages (predicate occurrences).
        """
        return sum(self.property_frequencies.values())

    @property
    def num_object_properties(
        self
        ) -> int:
        """
        Returns the number of distinct object properties used in the graph.
        """
        return len(self.object_properties)
    
    @property
    def num_data_properties(
        self
        ) -> int:
        """
        Returns the number of distinct data (literal) properties used in the graph.
        """
        return len(self.data_properties)

    @property
    def num_classes(
        self
        ) -> int:
        """
        Returns the number of distinct RDF classes used in rdf:type statements.
        """
        return len(self.class_frequencies)

    @property
    def num_models(
        self
        ) -> int:
        """
        Returns the number of distinct models (namespaces) used in the graph.
        """
        return len(self.model_frequencies)

    @property
    def most_frequent_properties(
        self,
        n: int = 10
        ) -> List[Tuple[str, int]]:
        """
        Returns the top `n` most frequently used properties.

        Args:
            n (int): The number of top properties to return. Default is 10.

        Returns:
            List[Tuple[str, int]]: A list of (property URI, frequency) tuples.
        """
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
        """
        Returns the top `n` most frequently assigned classes.

        Args:
            n (int): The number of top classes to return. Default is 10.

        Returns:
            List[Tuple[str, int]]: A list of (class URI, frequency) tuples.
        """
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
        """
        Returns the top `n` most frequently used models (namespaces).

        Args:
            n (int): The number of top models to return. Default is 10.

        Returns:
            List[Tuple[str, str, int]]: A list of (prefix, namespace URI, frequency) tuples.
        """
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
        """
        Returns a dictionary summarizing the basic statistics of the graph.

        Returns:
            dict: A dictionary containing key graph statistics:
                  - number of triples
                  - number of entities
                  - number of properties
                  - number of unique object properties
                  - number of unique data properties
                  - number of classes
                  - number of models (ontologies and controlled vocabularies declared)
        """
        return {
            "num_triples": self.num_triples,
            "num_entities": self.num_entities,
            "num_properties": self.num_properties,
            "num_object_properties": self.num_object_properties,
            "num_data_properties": self.num_data_properties,
            "num_classes": self.num_classes,
            "num_models": self.num_models
        }
