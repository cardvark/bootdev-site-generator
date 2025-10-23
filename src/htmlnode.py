class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):

        output_string = ""
        
        for k, v in self.props.items():
            # print(f"k: {k}, v: {v}")
            output_string += f' {k}="{v}"'
    
        return output_string

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    # HTMLNode that should ALWAYS have value, and NEVER have children.
    # props are optional.

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("No value found. All leaf nodes must have values.")
        if self.tag == None:
            return f"{self.value}"
        
        output_string = "<"
        output_string += self.tag
        if self.props:
            output_string += self.props_to_html()
        output_string += ">"
        output_string += self.value
        output_string += f"</{self.tag}>"

        return output_string

class ParentNode(HTMLNode):
    # HTMLNode that should NEVER have values, and must ALWAYS have children.
    # props are optional.

    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("No tag found. All parent nodes must have a tag.")
        
        if not self.children:
            raise ValueError("No children found. All parent nodes must have children.")
        
        output_string = ""
        output_string += f"<{self.tag}"
        if self.props:
            output_string += self.props_to_html()
        output_string += ">"
        for child in self.children:
            output_string += child.to_html()
        
        output_string += f"</{self.tag}>"

        return output_string
