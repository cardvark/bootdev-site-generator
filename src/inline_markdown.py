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


def split_nodes_image(old_nodes):
    # take a list of nodes and extract image specific nodes.

    output_list = []
    
    for old_node in old_nodes:
        image_node_tuples = extract_markdown_images(old_node.text)
        # print(f"For old_node: {old_node}, \nprinting extracted image node tuples: \n{image_node_tuples}")
       
        if not image_node_tuples:
            # print(f"No image nodes found in old_node. Appending old node:\n{old_node}")
            output_list.append(old_node)
            continue

        old_text = old_node.text

        for image_node in image_node_tuples:
            # print(f"On image node: {image_node}")
            sections = old_text.split(f"![{image_node[0]}]({image_node[1]})", 1)

            # print(sections)

            if sections[0]:
                output_list.append(
                    TextNode(sections[0], old_node.text_type)
                )
            
            old_text = sections[1]
            output_list.append(
                TextNode(image_node[0], TextType.IMAGE, image_node[1])
            )

        if old_text:
            output_list.append(TextNode(old_text, old_node.text_type))
    
    return output_list

def split_nodes_link(old_nodes):
    # take a list of nodes and extract link specific nodes.

    output_list = []
    
    for old_node in old_nodes:
        link_node_tuples = extract_markdown_links(old_node.text)
       
        if not link_node_tuples:
            output_list.append(old_node)
            continue

        old_text = old_node.text

        for link_node in link_node_tuples:
            # print(f"On image node: {link_node}")
            sections = old_text.split(f"[{link_node[0]}]({link_node[1]})", 1)

            # print(sections)

            if sections[0]:
                output_list.append(
                    TextNode(sections[0], old_node.text_type)
                )

            old_text = sections[1]
            output_list.append(
                TextNode(link_node[0], TextType.LINK, link_node[1])
            )

        if old_text:
            output_list.append(TextNode(old_text, old_node.text_type))
    
    return output_list