import unittest

from textnode import TextNode


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

if __name__ == "__main__":
    unittest.main()