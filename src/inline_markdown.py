from textnode import TextNode, TextType
import re
    
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



def extract_markdown_images(text):
    # takes raw markdown text and returns list of tuples.
    # each tuple contains the (alt text, url) of each img

    # E.g. text: text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    # takes raw markdown text and returns list of tuples
    # each tuple contains the (anchor text, url) of each link

    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)

