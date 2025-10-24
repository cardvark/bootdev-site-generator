import unittest

from textnode import TextNode, TextType
from inline_markdown import * 

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
class TestMarkdownExtraction(unittest.TestCase):
    print("\n\nRunning tests on image and link extraction from markdown text.")

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_link(self):
        matches = extract_markdown_links(
            "This is text with a link of a [banana](www.banana.com)."
        )
        self.assertListEqual(
            [("banana", "www.banana.com")],
            matches
        )
    
    def test_extract_only_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link of a [banana](www.banana.com)."
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_only_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link of a [banana](www.banana.com)."
        )
        self.assertListEqual(
            [("banana", "www.banana.com")],
            matches
        )

    def test_extract_multiple_links_only(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link of a [banana](www.banana.com). and a link of a [potato](www.potato.com)"
        )
        self.assertListEqual(
            [
                ("banana", "www.banana.com"),
                ("potato", "www.potato.com")
            ],
            matches
        )
        
    
class TestImageAndLinkNodeSplitting(unittest.TestCase):
    print("\n\nRunning tests on image node extraction")

    def test_images_in_plain_text(self):
        print("\n\nTesting images in plain text.")
        plain_text_nodes = [
            TextNode("This has an image of a ![cat](www.cat.com) and a ![dog](www.dog.com).", TextType.PLAIN),
            TextNode("This has an image of a ![tarantula](www.tarantula.com).", TextType.PLAIN),
            TextNode("This one has no images.", TextType.PLAIN)
        ]

        new_nodes = split_nodes_image(plain_text_nodes)

        for node in new_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("This has an image of a ", TextType.PLAIN),
                TextNode("cat", TextType.IMAGE, "www.cat.com"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("dog", TextType.IMAGE, "www.dog.com"),
                TextNode(".", TextType.PLAIN),
                TextNode("This has an image of a ", TextType.PLAIN),
                TextNode("tarantula", TextType.IMAGE, "www.tarantula.com"),
                TextNode(".", TextType.PLAIN),
                TextNode("This one has no images.", TextType.PLAIN),
            ],
            new_nodes,
        )
    
    def test_links_in_plain_text(self):
        print("\n\nTesting links in plain text.")
        plain_text_nodes = [    
            TextNode("This has a link to a [silly blog post](www.sillypost.com).", TextType.PLAIN),
            TextNode("This one has no links.", TextType.PLAIN),
            TextNode("This has a link to a [silly blog post](www.sillypost.com) and a [smart post](www.smartpost.com).", TextType.PLAIN)
        ]

        new_nodes = split_nodes_link(plain_text_nodes)

        for node in new_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("This has a link to a ", TextType.PLAIN),
                TextNode("silly blog post", TextType.LINK, "www.sillypost.com"),
                TextNode(".", TextType.PLAIN),
                TextNode("This one has no links.", TextType.PLAIN),
                TextNode("This has a link to a ", TextType.PLAIN),
                TextNode("silly blog post", TextType.LINK, "www.sillypost.com"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("smart post", TextType.LINK, "www.smartpost.com"),
                TextNode(".", TextType.PLAIN),
            ],
            new_nodes,
        )
    
    def test_links_starting(self):
        print("\n\nTesting links at start of plain text.")

        plain_text_nodes = [
            TextNode("[Starting link solo](www.link.com)", TextType.PLAIN),
            TextNode("[Starting sentence](www.sentence-link.com) with a link.",TextType.PLAIN)
        ]

        new_nodes = split_nodes_link(plain_text_nodes)

        for node in new_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("Starting link solo", TextType.LINK, "www.link.com"),
                TextNode("Starting sentence", TextType.LINK, "www.sentence-link.com"),
                TextNode(" with a link.", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_images_only_mixed(self):
        print("\n\nTesting image extraction in mixed image + link markdown text")

        plain_text_nodes = [
            TextNode("This is a link to a [blog post](www.blogpost.com) and a picture of a ![cute cat](www.cat-image-url.com).", TextType.PLAIN)
        ]

        new_nodes = split_nodes_image(plain_text_nodes)

        for node in new_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("This is a link to a [blog post](www.blogpost.com) and a picture of a ", TextType.PLAIN),
                TextNode("cute cat", TextType.IMAGE, "www.cat-image-url.com"),
                TextNode(".", TextType.PLAIN),
            ],
            new_nodes,
        )

    def test_links_only_mixed(self):
        print("\n\nTesting link extraction in mixed image + link markdown text")

        plain_text_nodes = [
            TextNode("This is a link to a [blog post](www.blogpost.com) and a picture of a ![cute cat](www.cat-image-url.com).", TextType.PLAIN)
        ]

        new_nodes = split_nodes_link(plain_text_nodes)

        for node in new_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("This is a link to a ", TextType.PLAIN),
                TextNode("blog post", TextType.LINK, "www.blogpost.com"),
                TextNode(" and a picture of a ![cute cat](www.cat-image-url.com).", TextType.PLAIN)  
            ],
            new_nodes,
        )
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        
        for node in new_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

class TestTextToNodes(unittest.TestCase):
    print("\n\nTesting full transformation function...")

    def test_simple_gamut(self):
        print("\n\nTesting a mixed line of marked down text.")

        
        raw_text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        processed_nodes = text_to_nodes(raw_text)

        for node in processed_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.PLAIN),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.PLAIN),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.PLAIN),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.PLAIN),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.PLAIN),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            processed_nodes
        )
    
    def test_single_image(self):
        print("\n\nTesting a single image.")
        single_image_text = "![alt text](www.url.com)"

        processed_nodes = text_to_nodes(single_image_text)

        for node in processed_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("alt text", TextType.IMAGE, "www.url.com")
            ],
            processed_nodes
        )
    
    def test_plain_text(self):
        print("\n\nTesting simple plain text.")
        plain_text = "This is some basic-ass text."

        processed_nodes = text_to_nodes(plain_text)

        for node in processed_nodes:
            print(node)

        self.assertListEqual(
            [
                TextNode("This is some basic-ass text.", TextType.PLAIN)
            ],
            processed_nodes
        )


    # TODO: support overlapping markdown formatting.

    # def test_overlapping_formatting(self):
    #     print("\n\nTesting overlapping formatting...")

    #     raw_text = "This is **bullshit _and_ [frankly](www.url.com)** unneccessary."

    #     processed_nodes = text_to_nodes(raw_text)

    #     for node in processed_nodes:
    #         print(node)

    #     self.assertListEqual(
    #         [
    #             TextNode("This is ", TextType.PLAIN),
    #             TextNode("bullshit ", TextType.BOLD),
    #             TextNode("and", TextType.ITALIC),
    #             TextNode(" ", TextType.BOLD),
    #             TextNode("frankly", TextType.LINK, "www.url.com"),
    #             TextNode("unnecessary.", TextType.PLAIN)
    #         ],
    #         processed_nodes
    #     )
    
    def test_empty_string(self):
        print("\n\nTesting empty string error...")

        empty_string = ""

        with self.assertRaises(Exception) as e:
            processed_nodes = text_to_nodes(empty_string)

        self.assertEqual(
            str(e.exception),
            "Must contained text."
        )


if __name__ == "__main__":
    unittest.main()