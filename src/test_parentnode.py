import unittest

from htmlnode import ParentNode, LeafNode

class TestParentNode(unittest.TestCase):
    print("\n\nrunning parent node tests...")

    def test_to_html_with_children(self):
        print("\n\nTesting to_html with children:")
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])

        html_output = parent_node.to_html()
        print(html_output)
        self.assertEqual(
            html_output,
            "<div><span>child</span></div>"
        )

    def test_to_html_with_grandchildren(self):
        print("\n\nTesting to html with grandchildren")
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])

        html_output = parent_node.to_html()
        print(html_output)
        self.assertEqual(
            html_output,
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_properties(self):
        print("\n\nTesting to html with grandchildren")
        grandchild_node = LeafNode("b", "grandchild", {"id": "grand_child_node", "class": "b-tainer"})
        child_node = ParentNode("span", [grandchild_node], {"id": "child_node", "class": "spantainer"})
        parent_node = ParentNode("div", [child_node], {"id": "parent_node", "class": "divtainer"})

        html_output = parent_node.to_html()
        print(html_output)
        self.assertEqual(
            html_output,
            '<div id="parent_node" class="divtainer"><span id="child_node" class="spantainer"><b id="grand_child_node" class="b-tainer">grandchild</b></span></div>',
        )

    def test_no_children_value_error(self):
        print("\n\nTesting error when parent node has no children")
        no_kids_parent = ParentNode("a", [])

        with self.assertRaises(ValueError) as e:
            no_kids_parent.to_html()

        self.assertEqual(
            str(e.exception),
            "No children found. All parent nodes must have children."
        )
    
    def test_no_tag_value_error(self):
        print("\n\nTesting error when parent node has no tag")
        child_node = LeafNode("span", "child")
        no_tag_parent = ParentNode("", [child_node])

        with self.assertRaises(ValueError) as e:
            no_tag_parent.to_html()

        self.assertEqual(
            str(e.exception),
            "No tag found. All parent nodes must have a tag."
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )