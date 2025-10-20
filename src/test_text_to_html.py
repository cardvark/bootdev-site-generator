import unittest

from textnode import TextType, TextNode, text_node_to_html_node

class TestTextToHTML(unittest.TestCase):
    print("\n\nRunning text to html tests...")

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        print(f"\n\nTesting plain text node: \n{node}")
        html_node = text_node_to_html_node(node)
        print(f"\n\n Plain text --> html: \n{html_node}")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        bold_node = TextNode("This is a bolded text node", TextType.BOLD)
        print(f"\n\nTesting bold text node: \n{bold_node}")
        html_node = text_node_to_html_node(bold_node)
        print(f"\n\n Bold text --> html: \n{html_node}")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bolded text node")

    def test_link_text(self):
        link_node = TextNode(
            "This is a link node", 
            TextType.LINK, 
            "www.a-website.com"
        )
        print(f"\n\nTesting link text node: \n{link_node}")
        html_node = text_node_to_html_node(link_node)
        print(f"\n\n Link text --> html: \n{html_node}")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "www.a-website.com",})
        
    def test_image_text(self):
        image_node = TextNode(
            "This is an image node",
            TextType.IMAGE, 
            "www.img-src-url"
        )
        print(f"\n\nTesting image text node: \n{image_node}")
        html_node = text_node_to_html_node(image_node)
        print(f"\n\n Image text --> html: \n{html_node}")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, 
            {
                "src": "www.img-src-url",
                "alt": "This is an image node"
            }
        )
