import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props = {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_no_props(self):
        node = HTMLNode(value = "This is some text.")
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props(self):
        node = HTMLNode(props = {})
        self.assertEqual(node.props_to_html(), "")