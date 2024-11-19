import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_raw(self):
        node = LeafNode("This is some text.")
        self.assertEqual(node.to_html(), "This is some text.")

    def test_tagged(self):
        node = LeafNode("This is bold text.", tag = "b")
        self.assertEqual(node.to_html(), "<b>This is bold text.</b>")

    def test_props(self):
        node = LeafNode("This is Google.", tag = "a", props = {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">This is Google.</a>')

    def test_error(self):
        node = LeafNode(None, tag = "i")
        with self.assertRaises(ValueError):
            html = node.to_html()