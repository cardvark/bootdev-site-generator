from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    PLAIN = "plain text"
    BOLD = "bold text"
    ITALIC = "italic text"
    CODE = "code text"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        return (self.text == other_node.text
            and self.text_type == other_node.text_type
            and self.url == other_node.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type not in TextType:
        raise ValueError("Text type not supported.")

    text = text_node.text
    
    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text)
        case TextType.BOLD:
            return LeafNode("b", text)
        case TextType.ITALIC:
            return LeafNode("i", text)
        case TextType.CODE:
            return LeafNode("code", text)
        case TextType.LINK:
            return LeafNode(
                "a", text, 
                {"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                "img", 
                "", 
                {
                    "src": text_node.url, 
                    "alt": text_node.text
                }
            )
