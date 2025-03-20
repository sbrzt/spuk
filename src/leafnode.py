from htmlnode import HTMLNode


class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.tag:
            if not self.value:
                raise ValueError("Value must exist.")
            return self.value
        else:
            self_closing_tags = {
                "img",
                "br"
            }
            if self.tag in self_closing_tags:
                return f"<{self.tag}{self.props_to_html() if self.props else ''}/>"
            if not self.value:
                raise ValueError("Value must exist.")
            return f'<{self.tag}{self.props_to_html() if self.props else ""}>{self.value}</{self.tag}>'
