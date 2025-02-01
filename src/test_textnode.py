import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("this is a text node", TextType.NORMAL)
        node2 = TextNode("this is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_images(self):
        node = TextNode("this is a text node", TextType.IMAGE, "./my_image.png")
        node2 = TextNode("this is a text node", TextType.IMAGE, "./my_image.jpg")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
