from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    return [line.strip() for line in blocks if line != ""]


def line_checker(block_lines, reg_pattern):
    for line in block_lines:
        if not re.search(reg_pattern, line):
            return False
    
    return True


def block_to_block_type(block):
    
    #check if HEADING
    if re.search(r"^#{1,6} ", block):
        return BlockType.HEADING

    if re.search(r"^```.*```$", block, re.DOTALL):
        return BlockType.CODE

    block_lines = block.split("\n")

    quote_pattern = r"^>"
    unordered_list_pattern = r"- "
    number_pattern = r"^\d+\. "

    if line_checker(block_lines, quote_pattern):
        return BlockType.QUOTE

    if line_checker(block_lines, unordered_list_pattern):
        return BlockType.UNORDERED_LIST

    if line_checker(block_lines, number_pattern):
        start = 1
        for line in block_lines:
            digit = re.match(r"^\d+", line)
            if not int(digit.group(0)) == start:
                return BlockType.PARAGRAPH
            start += 1
        
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

