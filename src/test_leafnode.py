import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_1(self):
        node = LeafNode("a", "Link", {"href": "https://www.example.org", "target": "_blank"})
        assert node.to_html() == '<a href="https://www.example.org" target="_blank">Link</a>'
    def test_to_html_2(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError):
            node.to_html()
    def test_to_html_3(self):
        node = LeafNode(None, "Text")
        assert node.to_html() == "Text"
    

if __name__ == "__main__":
    unittest.main()