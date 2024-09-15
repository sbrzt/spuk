from leafnode import LeafNode


def text_node_to_html_node(text_node):
    
    match text_node.text_type:
        case "text":
            leaf_node = LeafNode(
                None,
                text_node.text
            )
        case "bold":
            leaf_node = LeafNode(
                "b",
                text_node.text
            )
        case "italic":
            leaf_node = LeafNode(
                "i",
                text_node.text
            )
        case "code":
            leaf_node = LeafNode(
                "code",
                text_node.text
            )
        case "link":
            leaf_node = LeafNode(
                "a",
                text_node.text,
                {"href": text_node.url}
            )
        case "image":
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