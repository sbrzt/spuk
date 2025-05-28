import os
import shutil
import tempfile
import unittest
from rdflib import Graph, URIRef, Literal, RDF, Namespace
from src.entity_object import EntityObject
from src.models import EntityData, PropertyValuePair
from src.knowledge_graph import KnowledgeGraph

EX = Namespace("http://example.org/kg/")


class ProxyKnowledgeGraph(KnowledgeGraph):
    def __init__(self, graph: Graph):
        self._graph = graph

    def get_graph(self):
        return self._graph


class TestEntityObject(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.graph = Graph()
        self.graph.bind("ex", EX)
        self.graph.add((EX.alice, RDF.type, EX.Person))
        self.graph.add((EX.alice, EX.age, Literal("30")))
        self.graph.add((EX.alice, EX.knows, EX.bob))
        snippet = self.graph
        self.graph.add((EX.bob, RDF.type, EX.Person))
        self.kg = ProxyKnowledgeGraph(self.graph)

        self.entity_data = EntityData(
            uri = str(EX.alice),
            types = [str(EX.Person)],
            properties = [
                PropertyValuePair(
                    property_uri = str(EX.age),
                    property_label = "age",
                    value = "30",
                    is_literal = True
                ),
                PropertyValuePair(
                    property_uri = str(EX.knows),
                    property_label = "knows",
                    value = str(EX.bob),
                    is_literal = False
                )
            ],
            snippet = snippet
        )

        self.entity = EntityObject(self.entity_data)
        self.entity.path = os.path.join(self.tmp_dir, "alice")
        self.entity.base_path = self.tmp_dir
    
    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_init(self):
        self.assertEqual(self.entity.uri, str(EX.alice))
        self.assertEqual(len(self.entity.properties), 2)
        self.assertIn(str(EX.Person), self.entity.types)
        self.assertIsInstance(self.entity.snippet, Graph)

    def test_generate_folders(self):
        self.entity.generate_folders()
        self.assertTrue(os.path.exists(self.entity.path))
        self.assertTrue(os.path.isdir(self.entity.path))

    def test_serialize(self):
        self.entity.generate_folders()
        self.entity.serialize()
        for ext in ["ttl", "nt", "xml", "jsonld"]:
            file_path = os.path.join(self.entity.path, "alice." + ext)
            self.assertTrue(os.path.exists(file_path), f"{ext} file missing")

    def test_render(self):
        html = self.entity.render()
        self.assertIn("http://example.org/kg/alice", html)
        self.assertIn("age", html)
        self.assertIn("knows", html)
        self.assertIn("bob", html)
    
    def test_save(self):
        self.entity.generate_folders()
        self.entity.save()
        html_path = os.path.join(self.entity.path, "alice.html")
        self.assertTrue(os.path.exists(html_path))
        with open(html_path, "r", encoding="utf-8") as f:
            contents = f.read()
        self.assertIn("http://example.org/kg/alice", contents)


if __name__ == '__main__':
    unittest.main()