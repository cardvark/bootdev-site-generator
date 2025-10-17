import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne(self):
        node = TextNode("This is the same text", TextType.PLAIN)
        node2 = TextNode("This is the same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_print(self):
        node = TextNode("Link check", TextType.LINK, "www.whatever.com")
        print(node)

        

if __name__ == "__main__":
    unittest.main()
