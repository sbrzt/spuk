import unittest
from src.rdf_graph import RDFGraph
from rdflib import URIRef

class TestRDFGraph(unittest.TestCase):
    def setUp(self):
        self.graph = RDFGraph("data/data.ttl")

    def test_get_entities_returns_uris(self):
        entities = self.graph.get_entities()
        self.assertTrue(all(isinstance(i, URIRef) for i in entities))

    def test_get_properties_returns_triples(self):
        subject = next(iter(self.graph.get_entities()))
        properties = self.graph.get_properties(subject)
        self.assertTrue(all(len(t) == 2 for t in properties))

if __name__ == "__main__":
    unittest.main()
