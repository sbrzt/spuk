from htmlnode import HTMLNode


class ParentNode(HTMLNode):

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError("Missing children")
        strng = ""
        for node in self.children:
            strng += node.to_html()
        return f"<{self.tag}{self.props_to_html() if self.props else ''}>{strng}</{self.tag}>"
