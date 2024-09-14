from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self, value, tag=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("Value must exist.")
        if not self.tag:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html() if self.props else ""}>{self.value}</{self.tag}>'

    