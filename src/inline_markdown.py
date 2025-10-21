from textnode import TextNode, TextType
    
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


