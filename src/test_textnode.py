import unittest

from textnode import TextNode
from leafnode import LeafNode
from functions import text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is another text node", "italic", None)
        node2 = TextNode("This is another text node", "italic", None)
        self.assertEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is another text node", "bold")
        node2 = TextNode("This is another text node", "italic")
        self.assertNotEqual(node, node2)
    def test_eq4(self):
        node = TextNode("This is another text node", "bold", "https://www.example.org")
        node2 = TextNode("This is another text node", "bold", "https://www.example.org")
        self.assertEqual(node, node2)
    def test_eq5(self):
        node = TextNode("This is another text node", "bold", None)
        node2 = TextNode("This is another text node", "bold", "https://www.example.org")
        self.assertNotEqual(node, node2)

    def test_text_to_html_text(self):
        node = TextNode("This is another text node", "text", None)
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode(None, "This is another text node")
        )

    def test_text_to_html_bold(self):
        node = TextNode("This is another text node", "bold", None)
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("b", "This is another text node")
        )
    
    def test_text_to_html_italic(self):
        node = TextNode("This is another text node", "italic", None)
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("i", "This is another text node")
        )

    def test_text_to_html_code(self):
        node = TextNode("This is another text node", "code", None)
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("code", "This is another text node")
        )

    def test_text_to_html_link(self):
        node = TextNode("This is another text node", "link", "https://www.example.org")
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("a", "This is another text node", {"href": "https://www.example.org"})
        )
    
    def test_text_to_html_image(self):
        node = TextNode("This is another text node", "image", "https://www.example.org")
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("img", "", {"src": "https://www.example.org", "alt": "This is another text node"})
        )
    
    def test_text_to_html_other(self):
        node = TextNode("This is another text node", "other", "https://www.example.org")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)

if __name__ == "__main__":
    unittest.main()