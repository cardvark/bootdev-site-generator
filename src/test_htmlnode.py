import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    print("running html node tests...")

    def test_args(self):
        para_node = HTMLNode("p", "Words and such")
        
        self.assertEqual(
            para_node.tag,
            "p"
        )

        self.assertEqual(
            para_node.value,
            "Words and such"
        )

        self.assertEqual(
            para_node.children,
            None
        )

        self.assertEqual(
            para_node.props,
            None
        )

    def test_print(self):
        para_node = HTMLNode("p", "Words and such")
        link_node = HTMLNode("a", "a link", None, {"href": "www.website.com", "target": "_blank"})
        parent_node = HTMLNode("p", None, para_node)
        
        print("\n\nPrinting paragraph node:")
        print(para_node)
        self.assertEqual(
            para_node.__repr__(),
            "HTMLNode(p, Words and such, children: None, None)"

        )
        print("\n\nPrinting link node:")
        print(link_node)
        print("\n\nPrinting parent node:")
        print(parent_node)

    def test_props_to_html(self):
        link_node = HTMLNode("a", "a link", None, {"href": "www.website.com", "target": "_blank"})
        print("\n\nPrinting link props to html")
        print(link_node.props_to_html())

        self.assertEqual(
            link_node.props_to_html(),
            'href="www.website.com" target="_blank"'
        )

    

    

if __name__ == "__main__":
    unittest.main()
