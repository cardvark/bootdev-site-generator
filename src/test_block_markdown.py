import unittest

from block_markdown import *

class TestMarkdownToBlocks(unittest.TestCase):
    print("\n\nRunning markdown to blocks tests...")

    def test_markdown_to_blocks(self):
        print("\n\nTesting a mixed 3 block markdown text.")
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        for block in blocks:
            print(block)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_single_block(self):
        print("\n\nTesting a single long line. with single newline breaks.")
        md = """
A line of text in a single block, no matter how long, is still but a single block.
In fact, adding a line does not negate this at all. 
A block requires double line breaks to be considered another block.
"""

        blocks = markdown_to_blocks(md)

        for block in blocks:
            print(block)

        self.assertEqual(
            blocks,
            [
                "A line of text in a single block, no matter how long, is still but a single block.\nIn fact, adding a line does not negate this at all. \nA block requires double line breaks to be considered another block."
            ],
        )


    def test_markdown_to_blocks(self):
        print("\n\nTesting a mixed 3 block markdown text with a bunch of extra newlines.")
        md = """
This is **bolded** paragraph







This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        blocks = markdown_to_blocks(md)
        for block in blocks:
            print(block)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockType(unittest.TestCase):
    print("\n\nTesting block to blocktype eval")

    def block_type_matcher(self, tests):
        for block, expected_output in tests:
            with self.subTest(item=block):
                print(f"\n\nTesting block:\n\n{block}\n\nExpecting output: {expected_output}")
                actual_output = block_to_block_type(block)
                print(f"Received output: {actual_output}")
                self.assertEqual(
                    actual_output, 
                    expected_output,
                    f"Failed for item: {block}"
                )

    def test_heading_blocks(self):
        print("\n\nTesting basic heading block")

        heading_tests = [
            ("# A simple heading block", BlockType.HEADING),
            ("### Another heading block", BlockType.HEADING),
            ("###### Longest headingh block", BlockType.HEADING),
            ("#Not a heading block.", BlockType.PARAGRAPH),
            ("####### Too long to be a heading block", BlockType.PARAGRAPH),
            ("Also not a heading block.", BlockType.PARAGRAPH),
        ]

        self.block_type_matcher(heading_tests)

    
    def test_code_blocks(self):
        print("\n\nTesting code blocks")

        code_tests = [
            ("```A perfect little code block```",BlockType.CODE),
            ("```Code block with \n multiple \n\n\n line breaks.```", BlockType.CODE),
            ("Not quite code block ``` has ticks in the middle and then end.```", BlockType.PARAGRAPH),
        ]

        self.block_type_matcher(code_tests)

    def test_quote_blocks(self):
        print("\n\nTesting quote blocks...")

        quote_tests = [
            (">The first line\n>the second line\n>Even the third line are all quotes.", BlockType.QUOTE),
            ("d>Not quite", BlockType.PARAGRAPH),
            (">First is\n>As is second\nBut not the third.", BlockType.PARAGRAPH)
        ]

        self.block_type_matcher(quote_tests)

    def test_unordered_list_blocks(self):
        print("\n\nTesting unordered list blocks...")

        unordered_list_tests = [
            ("- This is a proper\n- unordered list\n- of items.", BlockType.UNORDERED_LIST),
            ("- This is not quite\n- an unordered\n list of items.", BlockType.PARAGRAPH),
            ("- Neither is\n\n- this", BlockType.PARAGRAPH),
        ]

        self.block_type_matcher(unordered_list_tests)
    
    def test_ordered_list_blocks(self):
        print("\n\nTesting ordered list blocks...")

        ordered_list_tests = [
            ("1. This is a properly\n2. Ordered list\n3. of items.", BlockType.ORDERED_LIST),
            ("1. This is not quite\n5.A proper list\n6. of items", BlockType.PARAGRAPH),
            ("1.neither is this\n2. lol.", BlockType.PARAGRAPH),
            ("1. This\n2. is so\n3. Tedious\n4. But I have\n5. To check\n6. if this goes to \n7. a higher\n8. digit\n9. than single\n10. and here it is", BlockType.ORDERED_LIST),
        ]

        self.block_type_matcher(ordered_list_tests)