import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_1(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        assert node.to_html() == '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
    
    def test_to_html_2(self):
        node = ParentNode(None, [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_3(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_4(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
        ])
        assert node.to_html() == '<p><b>Bold text</b></p>'

    def test_to_html_5(self):
        node = ParentNode("p", 
            [
                ParentNode("span", 
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ]
                ),
            ])
        assert node.to_html() == '<p><span><b>Bold text</b>Normal text</span></p>'

    def test_to_html_6(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
        ], {"class": "paragraph"})
        assert node.to_html() == '<p class="paragraph"><b>Bold text</b></p>'

    def test_to_html_7(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text", {"class": "strong"}),
        ], {"class": "paragraph"})
        assert node.to_html() == '<p class="paragraph"><b class="strong">Bold text</b></p>'

    def test_to_html_8(self):
        node = ParentNode("p", 
            [
                ParentNode("span", 
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                    ],
                    {
                        "class": "chunk"
                    }
                ),
            ], {"class": "paragraph"})
        assert node.to_html() == '<p class="paragraph"><span class="chunk"><b>Bold text</b>Normal text</span></p>'

if __name__ == "__main__":
    unittest.main()