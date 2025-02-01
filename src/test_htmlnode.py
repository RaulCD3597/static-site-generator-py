import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_props_to_html(self):
        node = HTMLNode("p", "this is a paragraph", props={})
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_no_props_to_html(self):
        node = HTMLNode("p", "this is a paragraph")
        expected = ""
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "google.com",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)


if __name__ == "__main__":
    unittest.main()
