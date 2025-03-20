import unittest
from htmlnode import HTMLNode
from blocktype import BlockType
from functions import extract_markdown_images, extract_markdown_links, markdown_to_blocks, block_to_block_type, text_to_children, block_type_to_html_node, markdown_to_html_node, extract_title


class TestFunctions(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_markdown_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        blocks = [
            "## heading 2",
            "```code block\nanother code```",
            "> This is\n>a quote\n>for me",
            "- first\n- second\n- third",
            "1. first\n2. second\n3. third",
            "this is just a paragraph"
        ]
        block_types = []
        for block in blocks:
            block_type = block_to_block_type(block)
            block_types.append(block_type)
        self.assertEqual(
            block_types,
            [
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.QUOTE,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH
            ],
        )

    def test_block_type_to_html_node_01(self):
        text = """```This is
        a code block```"""
        html_node = block_type_to_html_node(BlockType.CODE, text)
        self.assertEqual(
            html_node,
            HTMLNode("pre", None, [HTMLNode("code", None, [HTMLNode(None, "This is\na code block", None, None)], None)], None)
        )
        

    def test_block_type_to_html_node_02(self):
        text = """> This is a blockquote
        >
        > help"""
        html_node = block_type_to_html_node(BlockType.QUOTE, text)
        print(html_node)
        self.assertEqual(
            html_node,
            HTMLNode("blockquote", None, [HTMLNode("p", None, [HTMLNode(None, "This is a blockquote", None, None)], None), HTMLNode("p", None, [HTMLNode(None, "help", None, None)], None)], None)
        )

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph text in a p tag here

        This is another paragraph with _italic_ text and `code` here

        """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """```This is text that _should_ remain
        the **same** even with inline stuff```
        """
        node = markdown_to_html_node(md)
        self.assertEqual(
            node,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_extract_title_1(self):
        md = """# This is a title 

        This is not a title
        """
        title = extract_title(md)
        self.assertEqual(
            title,
            "This is a title",
        )

    def test_extract_title_2(self):
        md = """#This is not a working title 
        """
        with self.assertRaises(Exception):
           extract_title(md)


if __name__ == "__main__":
    unittest.main()