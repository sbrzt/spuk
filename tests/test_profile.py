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
        person = URIRef(ex + "Person")
        knows = URIRef(ex + "knows")
        age = URIRef(ex + "age")

        self.graph.add((alice, RDF.type, person))
        self.graph.add((bob, RDF.type, person))
        self.graph.add((alice, knows, bob))
        self.graph.add((alice, age, Literal(30)))

        self.kg = ProxyKnowledgeGraph(self.graph)
        self.profile = Profile(self.kg)

    def test_num_triples(self):
        self.assertEqual(self.profile.num_triples, 4)

    def test_num_entities(self):
        self.assertEqual(self.profile.num_entities, 2)

    def test_num_object_properties(self):
        self.assertEqual(self.profile.num_object_properties, 1)

    def test_num_data_properties(self):
        self.assertEqual(self.profile.num_data_properties, 1)

    def test_get_summary(self):
        summary = self.profile.get_summary()
        self.assertEqual(summary["num_triples"], 4)
        self.assertEqual(summary["num_entities"], 2)
        self.assertEqual(summary["num_object_properties"], 1)
        self.assertEqual(summary["num_data_properties"], 1)


if __name__ == "__main__":
    unittest.main()