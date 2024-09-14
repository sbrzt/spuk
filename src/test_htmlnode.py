import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode("a", "Link", None, {"href": "https://www.example.org", "target": "_blank"})
        assert node.props_to_html() == ' href="https://www.example.org" target="_blank"'
    def test_props_to_html_2(self):
        node = HTMLNode("a", "Link")
        assert node.props_to_html() == None

if __name__ == "__main__":
    unittest.main()