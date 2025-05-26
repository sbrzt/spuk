import unittest
from unittest.mock import patch, MagicMock
from src.knowledge_graph import KnowledgeGraph
import tempfile
import os
from rdflib import Graph, URIRef


class TestKnowledgeGraph(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            delete=False, 
            mode="w", 
            suffix=".ttl"
        )
        self.temp_file.write("""
            @prefix ex: <http://example.org/> .
            ex:subject ex:predicate ex:object .
        """)
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_load_from_file(self):
        kg = KnowledgeGraph(source=self.temp_file.name)
        g = kg.get_graph()
        self.assertIsInstance(g, Graph)
        self.assertEqual(len(g), 1)


class TestKnowledgeGraphSPARQLEndpoint(unittest.TestCase):

    @patch("src.knowledge_graph.SPARQLWrapper")
    def test_load_from_sparql(self, mock_sparql_wrapper):
        mock_response = MagicMock()
        mock_response.decode.return_value = """
            @prefix ex: <http://example.org/> .
            ex:subject ex:predicate ex:object .
        """
        mock_query_result = MagicMock()
        mock_query_result.convert.return_value = mock_response

        mock_instance = MagicMock()
        mock_instance.query.return_value = mock_query_result
        mock_sparql_wrapper.return_value = mock_instance

        kg = KnowledgeGraph(
            source="http://fake-endpoint.org", 
            is_sparql_endpoint=True
        )
        g = kg.get_graph()
        self.assertIsInstance(g, Graph)
        self.assertEqual(len(g), 1)


if __name__ == "__main__":
    unittest.main()