from htmlnode import HTMLNode
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import TextNode, TextType
from blocktype import BlockType
import re
import os


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


def split_nodes_image(old_nodes):
    """
    It takes a list of "old nodes". It should return a new list of nodes, 
    where any "text" type nodes in the input list are (potentially) split into multiple nodes that are either texts or images.
    """

    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if not images:
            new_nodes.append(old_node)
        else:
            current_text = old_node.text
            for image in images:
                text_parts = current_text.split(f"![{image[0]}]({image[1]})", 1)
                if text_parts[0]:
                    new_nodes.append(TextNode(text_parts[0], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                current_text = text_parts[1]
            if current_text:
                new_nodes.append(TextNode(current_text, TextType.TEXT))                         
    return new_nodes


def text_to_textnodes(text):
    textnode = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([textnode], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    """
    It takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings.
    """
    
    result = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        block = block.strip()
        if block:
            lines = block.split("\n")
            cleaned_lines = [line.strip() for line in lines]
            cleaned_block = "\n".join(cleaned_lines)
            result.append(cleaned_block)
    return result


def block_to_block_type(markdown):
    lines = markdown.split("\n")
    match markdown:
        case markdown if re.search("^#{1,6}\s{1}.+$", markdown):
            return BlockType.HEADING
        case markdown if re.search("^`{3}", lines[0]) and re.search("`{3}$", lines[-1]):
            return BlockType.CODE
        case markdown if all(re.search("^\>", line) for line in lines):
            return BlockType.QUOTE
        case markdown if all(re.search("^\- .+$", line) for line in lines):
            return BlockType.UNORDERED_LIST
        case markdown if all(re.search("^\d\. .+$", line) for line in lines):
            return BlockType.ORDERED_LIST
        case _:
            return BlockType.PARAGRAPH


def block_type_to_html_node(block_type, markdown):
    match block_type:
        case BlockType.HEADING:
            hashes = len(markdown) - len(markdown.lstrip("#"))
            markdown = markdown[hashes:].strip()
            return LeafNode(f"h{hashes}", markdown)
        case BlockType.QUOTE:
            lines = markdown.split("\n")
            quote = ""
            for line in lines:
                line = re.sub(r"^\>\s?", "", line.strip())
                quote += line + "\n"
            paragraphs = re.split(r"\n\s*\n", quote.strip())
            children = []
            for paragraph in paragraphs:
                if paragraph.strip():
                    p_node = ParentNode("p", text_to_children(paragraph.strip()))
                    children.append(p_node)
            return ParentNode("blockquote", children=children)
        case BlockType.UNORDERED_LIST:
            return lines_to_children(markdown, "ul")
        case BlockType.ORDERED_LIST:
            return lines_to_children(markdown, "ol")
        case BlockType.CODE:
            markdown = re.sub(r"^`{3}|`{3}$", "", markdown)
            lines = markdown.split("\n")
            clean = ""
            for i, line in enumerate(lines):
                if i < len(lines) - 1:
                    clean += line.strip() + "\n"
                else:
                    clean += line.strip()
            text_node = TextNode(clean.strip(), TextType.TEXT)
            html_node = text_node_to_html_node(text_node)
            code = ParentNode("code", children=[html_node])
            return ParentNode("pre", children=[code])
        case _:
            children = text_to_children(markdown)
            return ParentNode("p", children)


def lines_to_children(markdown, tag):
    lines = markdown.split("\n")
    lis = []
    for line in lines:
        line = re.sub(r"^\s*[-\d]+\.\s|\*\s|\-\s", "", line).strip()
        children = text_to_children(line)
        li = ParentNode("li", children=children)
        lis.append(li)
    return ParentNode(tag, children=lis)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_type_to_html_node(block_type, block)
        nodes.append(node)
    return ParentNode("div", children=nodes).to_html()


def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if re.match(r'^#{1} .+', line):
            line = line.replace('#', '').strip()
            return line
    raise Exception


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")
    with open(from_path, "r") as md:
        md_content = md.read()
        html_node = markdown_to_html_node(md_content)
        title = extract_title(md_content)
    with open(template_path, "r") as template:
        template_content = template.read()
        template_content = template_content.replace("{{ Title }}", title)
        template_content = template_content.replace("{{ Content }}", html_node)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    with open(dest_path, 'w') as file:
        file.write(template_content)
