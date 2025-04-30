import unittest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

class TestAPI(unittest.TestCase):
    def test_list_entities(self):
        response = client.get("/entities")
        self.assertEqual(response.status_code, 200)
        self.assertIn("entities", response.json())

    def test_get_entity(self):
        # NOTE: Adjust "Alice" to match one of your test entities
        response = client.get("/entities/Alice")
        self.assertEqual(response.status_code, 200)
        self.assertIn("subject", response.json())
        self.assertIn("properties", response.json())

    def test_get_invalid_entity(self):
        response = client.get("/entities/NotARealID")
        self.assertEqual(response.status_code, 404)

    def test_sparql_query_select(self):
        sparql = {
            "query": """
                SELECT ?s ?p ?o WHERE {
                    ?s ?p ?o .
                } LIMIT 1
            """
        }
        response = client.post("/sparql", json=sparql)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.json())

    def test_sparql_query_invalid(self):
        sparql = {"query": "BROKEN SPARQL"}
        response = client.post("/sparql", json=sparql)
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
