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
    
def split_node_delimeter(old_nodes, delimiter, text_type):
    output_list = []

    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            output_list.append(node)
            continue
        
        split_node = node.text.split(delimiter)

        if (len(split_node) % 2) != 1:
            raise Exception("Unmatched text modifier; invalid Markdown syntax.")
        
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue

            if i % 2 == 0:
                output_list.append(TextNode(split_node[i], TextType.PLAIN))
            else:
                output_list.append(TextNode(split_node[i], text_type))
    return output_list


