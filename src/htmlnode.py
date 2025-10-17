

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        output_list = []
        
        for k, v in self.props.items():
            # print(f"k: {k}, v: {v}")
            output_list.append(f'{k}="{v}"')
    
        return " ".join(output_list)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"