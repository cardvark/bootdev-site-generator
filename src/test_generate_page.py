import unittest

from generate_page import extract_title, generate_page

class TestExtractTitle(unittest.TestCase):
    print("\n\nTesting title extraction from markdown")

    def extracter(self, tests):
        for md, expected_output in tests:
            print(f"\n\nTesting markdown:\n{md}\n\nExpecting output:\n{expected_output}")

            with self.subTest(item=md):
                actual_output = extract_title(md)

                print(f"\nReceived output:\n{actual_output}")
                self.assertEqual(
                    actual_output,
                    expected_output,
                    f"Failed for item: {md}"
                )
    
    def test_basic_headers(self):
        basic_headers = [
            (
                "# Simple header 1",
                "Simple header 1"
            ),
            (
                "# Header only not \npast line break\nand strip all whitespace",
                "Header only not"
            ),
        ]

        self.extracter(basic_headers)

    
class TestGeneratePage(unittest.TestCase):
    print("\n\nTesting page generation...")

    def test_initial(self):
        path = "../content/index.md"
        template = "../template.html"
        dest_path = "../public/index.html"
        generate_page(path, template, dest_path)