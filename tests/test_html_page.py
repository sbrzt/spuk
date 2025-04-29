import unittest
import os
from src.html_page import HTMLPage
from rdflib import URIRef

class TestHTMLPage(unittest.TestCase):
    def test_save_creates_file(self):
        page = HTMLPage(URIRef("http://example.org/Alice"), [
            ("http://example.org/name", "Alice")
        ])
        page.save("docs")
        self.assertTrue(os.path.exists("docs/Alice.html"))

if __name__ == "__main__":
    unittest.main()
