import unittest
from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_nodes
from block_markdown import block_to_block_type, markdown_to_blocks, BlockType
from textnode import TextType, text_node_to_html_node
from markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    print("\n\nRunning markdown to HTML tests...")


    def markdown_to_html_checker(self, tests):
        for md, expected_output in tests:
            print(f"\n\nTesting markdown:\n{md}\n\nExpecting output:\n{expected_output}")

            with self.subTest(item=md):
                node = markdown_to_html_node(md)
                actual_output = node.to_html()
                print(f"Received output:\n{actual_output}")
                self.assertEqual(
                    actual_output,
                    expected_output,
                    f"Failed for item: {md}"
                )
        

    def test_paragraph_to_html(self):
        print("\n\nTesting basic paragraphs to html")

        paragraph_tests = [
            (
                "This is a **bolded** paragraph.\n\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line.", 
                "<div><p>This is a <b>bolded</b> paragraph.</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here This is the same paragraph on a new line.</p></div>",
            ),
        ]

        self.markdown_to_html_checker(paragraph_tests)


    def test_heading_blocks_to_html(self):
        print("\n\nTesting heading blocks to html.")

        heading_tests = [
            (
                "# A simple heading block.",
                "<div><h1>A simple heading block.</h1></div>"
            ),
            (
                "# First heading block.\n\n## Followed by a second.\n\n### Followed by a third.",
                "<div><h1>First heading block.</h1><h2>Followed by a second.</h2><h3>Followed by a third.</h3></div>"
            )
        ]

        self.markdown_to_html_checker(heading_tests)

    def test_code_blocks_to_html(self):
        print("\n\nTesting code blocks to html.")

        code_tests = [
            (
                "```\nCode block and whatnot\nGoes on and on.\n```",
                "<div><pre><code>Code block and whatnot\nGoes on and on.\n</code></pre></div>"
            ),
            (
                "```\nModified and **bolded** text\nand even _italicized_ text should retain the raw characters.\n```",
                "<div><pre><code>Modified and **bolded** text\nand even _italicized_ text should retain the raw characters.\n</code></pre></div>"
            ),
        ]

        self.markdown_to_html_checker(code_tests)
    
    
    def test_block_quote_to_html(self):
        print("\n\nTesting block quotes to html.")

        quote_tests = [
            (
                "> Each line of a quote\n> Must begin with a > symbol\n> To be considered a quote.",
                "<div><blockquote>Each line of a quote\nMust begin with a > symbol\nTo be considered a quote.</blockquote></div>"
            ),
            (
                "> Even within a quote however,\n> **Bolded** text should be bolded.\n> And _italicized_ text must be italicized.",
                "<div><blockquote>Even within a quote however,\n<b>Bolded</b> text should be bolded.\nAnd <i>italicized</i> text must be italicized.</blockquote></div>"
            )
        ]

        self.markdown_to_html_checker(quote_tests)

    def test_unordered_list_to_html(self):
        print("\n\nTesting unordered list to html.")

        unordered_tests = [
            (
                "- An unordered list\n- of items.\n- for stuff.",
                "<div><ul><li>An unordered list</li><li>of items.</li><li>for stuff.</li></ul></div>"
            ),
            (
                "- Another unordered list\n- But this one has **bolded** text\n- And even `code text`.",
                "<div><ul><li>Another unordered list</li><li>But this one has <b>bolded</b> text</li><li>And even <code>code text</code>.</li></ul></div>"
            )
        ]

        self.markdown_to_html_checker(unordered_tests)
    
    def test_ordered_list_to_html(self):
        print("\n\nTesting ordered list to html.")

        ordered_tests = [
            (
                "1. An ordered list.\n2. Has numbers in the front.\n3. That run in order.",
                "<div><ol><li>An ordered list.</li><li>Has numbers in the front.</li><li>That run in order.</li></ol></div>"
            ),
            (
                "1. An **ordered list**.\n2. Has numbers in the _front_.\n3. That run in [proper order](www.order-list.com).",
                '<div><ol><li>An <b>ordered list</b>.</li><li>Has numbers in the <i>front</i>.</li><li>That run in <a href="www.order-list.com">proper order</a>.</li></ol></div>'
            )
        ]

        self.markdown_to_html_checker(ordered_tests)
