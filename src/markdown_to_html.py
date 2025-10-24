from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_nodes
from block_markdown import block_to_block_type, markdown_to_blocks, BlockType
from textnode import TextType, text_node_to_html_node
import re


def text_nodes_to_html(text_nodes):
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    
    return html_nodes

def list_line_processor(text, ordered=False):
    lines = text.split("\n")
    reg_pattern = r"^\d+\. " if ordered else r"- "
    children_nodes = []

    for line in lines:
        clean_line = re.sub(reg_pattern, "", line)
        text_nodes = text_to_nodes(clean_line)
        leaf_nodes = text_nodes_to_html(text_nodes)
        line_parent = ParentNode("li", leaf_nodes)
        children_nodes.append(line_parent)

    return children_nodes

def text_to_children(text, block_type):
    if block_type == BlockType.UNORDERED_LIST:
        return list_line_processor(text)

    if block_type == BlockType.ORDERED_LIST:
        return list_line_processor(text, True)

    if block_type == BlockType.PARAGRAPH:
        text = text.replace('\n',' ')

    if block_type == BlockType.QUOTE:
        quote_lines = text.split("\n")
        new_lines = []
        for line in quote_lines:
            new_lines.append(line.lstrip("> "))
        
        text = "\n".join(new_lines)

    text_nodes = text_to_nodes(text)
    children_nodes = text_nodes_to_html(text_nodes)
    
    return children_nodes

def markdown_to_html_node(markdown):
    # takes markdown input and outputs a single parent HTMLNode that includes all relevant children.

    block_list = markdown_to_blocks(markdown)
    block_parents = []

    for block in block_list:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            children_nodes = text_to_children(block, block_type)
            parent_node = ParentNode("p", children_nodes)
            block_parents.append(parent_node)
        
        if block_type == BlockType.HEADING:
            header = re.search(r"^#{1,6} ", block).group(0)

            # Note: head_count includes the blank space after the # symbols.
            head_count = len(header)
            children_nodes = text_to_children(block[head_count:], block_type)
            parent_node = ParentNode(f"h{head_count - 1}", children_nodes)
            block_parents.append(parent_node)

        if block_type == BlockType.CODE:
            code_text = block[3:-3].lstrip()
            code_leaf = LeafNode("code", code_text)
            parent_node = ParentNode("pre", [code_leaf])
            block_parents.append(parent_node)

        if block_type == BlockType.QUOTE:
            children_nodes = text_to_children(block, block_type)
            parent_node = ParentNode("blockquote", children_nodes)
            block_parents.append(parent_node)

        if block_type == BlockType.UNORDERED_LIST:
            children_nodes = text_to_children(block, block_type)
            parent_node = ParentNode("ul", children_nodes)
            block_parents.append(parent_node)
        
        if block_type == BlockType.ORDERED_LIST:
            children_nodes = text_to_children(block, block_type)
            parent_node = ParentNode("ol", children_nodes)
            block_parents.append(parent_node)
    
    return ParentNode("div", block_parents)
                