import unittest

from textnode import TextNode, TextType, split_node_delimeter

class TestNodeSplitter(unittest.TestCase):
    print("\n\nrunning text node splitting tests...")

    def test_plaintext(self):
        plain_node = TextNode("This is a plain text node", TextType.PLAIN)
        new_nodes = split_node_delimeter([plain_node], "-", TextType.PLAIN)

        print(f"Testing plain text node: \n{plain_node}")
        # print(new_nodes)
        # print(new_nodes[0])

        self.assertEqual(
            new_nodes[0].__repr__(),
            "TextNode(This is a plain text node, plain text, None)"
        )
    
    def test_bolded_text(self):
        print("\n\n Running bold text splitting...")
        bold_text = "This text has been *bolded*."
        bold_node = TextNode(bold_text, TextType.PLAIN)
        already_bold = TextNode('This text is entirely bold', TextType.BOLD)
        new_nodes = split_node_delimeter([bold_node, already_bold], "*", TextType.BOLD)

        print(new_nodes)
        self.assertEqual(
            new_nodes,
            [
                TextNode('This text has been ', TextType.PLAIN),
                TextNode('bolded', TextType.BOLD),
                TextNode('.', TextType.PLAIN),
                TextNode('This text is entirely bold', TextType.BOLD)
            ]
        )

    def test_italicized_text_in_sequence(self):
        print("\n\n Running italicized text in sequence...")
        italicized1 = TextNode("This text has been _italicized_ more than _once_.", TextType.PLAIN)
        italicized2 = TextNode("This second string has _also_ been italicized _twice_.", TextType.PLAIN)

        new_nodes = split_node_delimeter([italicized1, italicized2], "_", TextType.ITALIC)

        self.assertEqual(
            new_nodes,
            [
                TextNode('This text has been ', TextType.PLAIN),
                TextNode('italicized', TextType.ITALIC),
                TextNode(' more than ', TextType.PLAIN),
                TextNode('once', TextType.ITALIC),
                TextNode('.', TextType.PLAIN),
                TextNode('This second string has ', TextType.PLAIN),
                TextNode('also', TextType.ITALIC),
                TextNode(' been italicized ', TextType.PLAIN),
                TextNode('twice', TextType.ITALIC),
                TextNode('.', TextType.PLAIN)
            ]
        )

    def test_missing_delimiter(self):
        print("\n\nTesting unmatched delimiter error...")

        missing_delimiter = TextNode('Open sided *bold is annoying.', TextType.PLAIN)

        

        with self.assertRaises(Exception) as e:
            new_nodes = split_node_delimeter([missing_delimiter], "*", TextType.BOLD)
        
        self.assertEqual(
            str(e.exception),
            "Unmatched text modifier; invalid Markdown syntax."
        )
    

if __name__ == "__main__":
    unittest.main()
