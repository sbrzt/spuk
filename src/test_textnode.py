import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from functions import text_node_to_html_node, split_nodes_delimiter, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is another text node", TextType.ITALIC, None)
        node2 = TextNode("This is another text node", TextType.ITALIC, None)
        self.assertEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is another text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_eq4(self):
        node = TextNode("This is another text node", TextType.BOLD, "https://www.example.org")
        node2 = TextNode("This is another text node", TextType.BOLD, "https://www.example.org")
        self.assertEqual(node, node2)
    def test_eq5(self):
        node = TextNode("This is another text node", TextType.BOLD, None)
        node2 = TextNode("This is another text node", TextType.BOLD, "https://www.example.org")
        self.assertNotEqual(node, node2)

    def test_text_to_html_text(self):
        node = TextNode("This is another text node", TextType.TEXT, None)
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode(None, "This is another text node")
        )

    def test_text_to_html_bold(self):
        node = TextNode("This is another text node", TextType.BOLD, None)
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("b", "This is another text node")
        )
    
    def test_text_to_html_italic(self):
        node = TextNode("This is another text node", TextType.ITALIC, None)
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("i", "This is another text node")
        )

    def test_text_to_html_code(self):
        node = TextNode("This is another text node", TextType.CODE, None)
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("code", "This is another text node")
        )

    def test_text_to_html_link(self):
        node = TextNode("This is another text node", TextType.LINK, "https://www.example.org")
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("a", "This is another text node", {"href": "https://www.example.org"})
        )
    
    def test_text_to_html_image(self):
        node = TextNode("This is another text node", TextType.IMAGE, "https://www.example.org")
        converted = text_node_to_html_node(node)
        self.assertEqual(
            converted, 
            LeafNode("img", "", {"src": "https://www.example.org", "alt": "This is another text node"})
        )

    def test_split_nodes_delimiter_01(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )
    
    def test_split_nodes_delimiter_02(self):
        node = TextNode("**Bold text** at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Bold text", TextType.BOLD),
                TextNode(" at the beginning", TextType.TEXT),
            ]
        )

    def test_split_nodes_delimiter_03(self):
        node = TextNode("Text that is _really_, _really_ intense", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text that is ", TextType.TEXT),
                TextNode("really", TextType.ITALIC),
                TextNode(", ", TextType.TEXT),
                TextNode("really", TextType.ITALIC),
                TextNode(" intense", TextType.TEXT),
            ]
        )

    def test_split_nodes_links_01(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ]
        )

    def test_split_nodes_links_02(self):
        node = TextNode("[Link at the beginning](https://www.boot.dev) and then nothing.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Link at the beginning", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and then nothing.", TextType.TEXT),
            ]
        )

    def test_split_nodes_links_03(self):
        node = TextNode("[Link at the beginning](https://www.boot.dev)[and immediately after](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Link at the beginning", TextType.LINK, "https://www.boot.dev"),
                TextNode("and immediately after", TextType.LINK, "https://www.boot.dev"),
            ]
        )

    def test_split_nodes_links_04(self):
        node = TextNode("Text at the beginning and [link only at the end](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("Text at the beginning and ", TextType.TEXT),
                TextNode("link only at the end", TextType.LINK, "https://www.boot.dev"),
            ]
        )

    def test_split_nodes_links_05(self):
        node = TextNode("No links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("No links", TextType.TEXT)
            ]
        )


if __name__ == "__main__":
    unittest.main()