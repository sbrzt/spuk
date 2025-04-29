import unittest
from src.rdf_graph import RDFGraph
from rdflib import URIRef

class TestRDFGraph(unittest.TestCase):
    def setUp(self):
        self.graph = RDFGraph("data/data.ttl")

    def test_get_individuals_returns_uris(self):
        individuals = self.graph.get_individuals()
        self.assertTrue(all(isinstance(i, URIRef) for i in individuals))

    def test_get_properties_returns_triples(self):
        subject = next(iter(self.graph.get_individuals()))
        properties = self.graph.get_properties(subject)
        self.assertTrue(all(len(t) == 2 for t in properties))

if __name__ == "__main__":
    unittest.main()
