import unittest

from htmlnode import LeafNode

class TestLeafNode(unittest.TestCase):
    print("running leaf node tests...")

    def test_instantiation(self):
        leaf_node = LeafNode("p", "Words and values")
        
        self.assertEqual(
            leaf_node.tag,
            "p"
        )
        
        self.assertEqual(
            leaf_node.value,
            "Words and values"
        )

        self.assertEqual(
            leaf_node.props,
            None
        )

        self.assertEqual(
            leaf_node.children,
            None
        )

    def test_leaf_with_props(self):
        link_leaf = LeafNode(
            "a", 
            "hyperlink text", 
            {
                "href": "www.google.com", 
                "target": "__whatever"
            }
        )

        self.assertEqual(
            link_leaf.tag,
            "a"
        )
        
        self.assertEqual(
            link_leaf.value,
            "hyperlink text"
        )

        self.assertEqual(
            link_leaf.props,
            {
                "href": "www.google.com", 
                "target": "__whatever"
            }
        )

        self.assertEqual(
            link_leaf.children,
            None
        )

        self.assertEqual(
            link_leaf.props_to_html(),
            ' href="www.google.com" target="__whatever"'
        )
    
    def test_to_html(self):
        link_leaf = LeafNode(
            "a", 
            "hyperlink text", 
            {
                "href": "www.google.com", 
                "target": "__whatever"
            }
        )

        self.assertEqual(
            link_leaf.to_html(),
            '<a href="www.google.com" target="__whatever">hyperlink text</a>'
        )

    def test_value_error(self):
        print("\n\nTesting leaf node value error.")
        bad_leaf = LeafNode(
            "p",
            None,
        )
        with self.assertRaises(ValueError) as e:
            bad_leaf.to_html()
        print(e.exception)
        self.assertEqual(
            str(e.exception),
            "No value found. All leaf nodes must have values."
        )
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

if __name__ == "__main__":
    unittest.main()
