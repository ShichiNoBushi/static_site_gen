import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("Text", TextType.NORMAL)
        self.assertEqual(node.text, "Text")

    def test_type(self):
        node = TextNode("Text", TextType.ITALIC)
        self.assertEqual(node.text_type, TextType.ITALIC)

    def test_url1(self):
        node = TextNode("Text", TextType.NORMAL)
        self.assertEqual(node.url, None)

    def test_ura2(self):
        node = TextNode("Text", TextType.NORMAL, "google.com")
        self.assertEqual(node.url, "google.com")

    def test_compare_text(self):
        node = TextNode("Text 1", TextType.NORMAL)
        node2 = TextNode("Text 2", TextType.NORMAL)
        self.assertNotEqual(node, node2)

    def test_compare_type(self):
        node = TextNode("Text", TextType.BOLD)
        node2 = TextNode("Text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_compare_url1(self):
        node = TextNode("Text", TextType.NORMAL, "yahoo.com")
        node2 = TextNode("Text", TextType.NORMAL, "youtube.com")
        self.assertNotEqual(node, node2)

    def test_compare_url2(self):
        node = TextNode("Text", TextType.NORMAL, "apple.com")
        node2 = TextNode("Text", TextType.NORMAL)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()