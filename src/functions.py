from leafnode import LeafNode
from textnode import TextNode, TextType
import re


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            leaf_node = LeafNode(
                None,
                text_node.text
            )
        case TextType.BOLD:
            leaf_node = LeafNode(
                "b",
                text_node.text
            )
        case TextType.ITALIC:
            leaf_node = LeafNode(
                "i",
                text_node.text
            )
        case TextType.CODE:
            leaf_node = LeafNode(
                "code",
                text_node.text
            )
        case TextType.LINK:
            leaf_node = LeafNode(
                "a",
                text_node.text,
                {"href": text_node.url}
            )
        case TextType.IMAGE:
            leaf_node = LeafNode(
                "img",
                "",
                {
                    "src": text_node.url,
                    "alt": text_node.text
                }
            )
        case _:
            raise Exception("Wrong type")
    
    return leaf_node


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    It takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, 
    where any "text" type nodes in the input list are (potentially) split into multiple nodes based on 
    the syntax.
    """

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        parts = old_node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception(f"Unmatched delimiter '{delimiter}' in text: {old_node.text}")
        for i, part in enumerate(parts):
            type_to_use = text_type if i % 2 == 1 else TextType.TEXT
            if part:
                new_nodes.append(TextNode(part, type_to_use))
    return new_nodes


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_link(old_nodes):
    """
    It takes a list of "old nodes". It should return a new list of nodes, 
    where any "text" type nodes in the input list are (potentially) split into multiple nodes that are either texts or links.
    """

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if not links:
            new_nodes.append(old_node)
        else:
            current_text = old_node.text
            for link in links:
                text_parts = current_text.split(f"[{link[0]}]({link[1]})", 1)
                if text_parts[0]:
                    new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                current_text = text_parts[1]
            if current_text:
                new_nodes.append(TextNode(current_text, TextType.TEXT))                         
    return new_nodes