import unittest
from rdflib import Graph, URIRef, Literal, RDF
from src.profile import Profile
from src.knowledge_graph import KnowledgeGraph
from src.models import EntityData, PropertyValuePair


class ProxyKnowledgeGraph(KnowledgeGraph):
    def __init__(
        self,
        graph: Graph
        ):
        self._graph = graph
    
    def get_graph(self):
        return self._graph
    

class TestProfile(unittest.TestCase):
    def setUp(
        self
        ):
        self.graph = Graph()

        ex = "http://example.org/"
        alice = URIRef(ex + "Alice")
        bob = URIRef(ex + "Bob")
        john = URIRef(ex + "John")
        person = URIRef(ex + "Person")
        dog = URIRef(ex + "Dog")
        knows = URIRef(ex + "knows")
        age = URIRef(ex + "age")

        self.graph.bind("ex", ex)

        self.graph.add((alice, RDF.type, person))
        self.graph.add((bob, RDF.type, person))
        self.graph.add((john, RDF.type, dog))
        self.graph.add((alice, knows, bob))
        self.graph.add((alice, knows, john))
        self.graph.add((alice, age, Literal(30)))

        self.kg = ProxyKnowledgeGraph(self.graph)
        self.profile = Profile(self.kg)

    def test_num_triples(self):
        self.assertEqual(self.profile.num_triples, 6)

    def test_num_entities(self):
        self.assertEqual(self.profile.num_entities, 3)

    def test_num_properties(self):
        self.assertEqual(self.profile.num_properties, 3)

    def test_num_object_properties(self):
        self.assertEqual(self.profile.num_object_properties, 1)

    def test_num_data_properties(self):
        self.assertEqual(self.profile.num_data_properties, 1)

    def test_num_classes(self):
        self.assertEqual(self.profile.num_classes, 2)

    def test_num_models(self):
        self.assertEqual(self.profile.num_models, 1)

    def test_most_frequent_properties(self):
        expected = [
            ("http://example.org/knows", 2),
            ("http://example.org/age", 1)
        ]
        result = self.profile.most_frequent_properties
        self.assertEqual(result, expected)

    def test_most_frequent_classes(self):
        expected = [
            ("http://example.org/Person", 2),
            ("http://example.org/Dog", 1)
        ]
        result = self.profile.most_frequent_classes
        self.assertEqual(result, expected)

    def test_most_frequent_models(self):
        expected = [
            ("ex", "http://example.org/", 6)
        ]
        result = self.profile.most_frequent_models
        self.assertEqual(result, expected)

    def test_get_summary(self):
        summary = self.profile.get_summary()
        self.assertEqual(summary["num_triples"], 6)
        self.assertEqual(summary["num_entities"], 3)
        self.assertEqual(summary["num_properties"], 3)
        self.assertEqual(summary["num_object_properties"], 1)
        self.assertEqual(summary["num_data_properties"], 1)
        self.assertEqual(summary["num_classes"], 2)
        self.assertEqual(summary["num_models"], 1)


if __name__ == "__main__":
    unittest.main()