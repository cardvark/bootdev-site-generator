import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    print("running text node tests...")
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

    def test_equal_link(self):
        node = TextNode("Link check", TextType.LINK, "www.whatever.com")
        node2 = TextNode("Link check", TextType.LINK, "www.whatever.com")
        self.assertEqual(node, node2)
    
    def test_equal_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        

if __name__ == "__main__":
    unittest.main()
