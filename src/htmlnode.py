class HTMLNode():
    
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and 
                self.value == other.value and 
                self.children == other.children and 
                self.props == other.props)

    def to_html(self):
        pass

    def props_to_html(self):
        if self.props:
            html_string = ""
            for item in self.props.items():
                html_string += f' {item[0]}="{item[1]}"'
            return html_string
