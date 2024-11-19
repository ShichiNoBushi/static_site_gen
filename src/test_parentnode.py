import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_fournode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("Bold text", "b"),
                LeafNode("Normal text", None),
                LeafNode("Italic text", "i"),
                LeafNode("Normal text", None)
            ]
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>")

    def test_parent_of_parents(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("Text 1", "b"),
                        LeafNode("Text 2", None)
                    ]
                ),
                ParentNode(
                    "i",
                    [
                        LeafNode("Text 3", "b"),
                        LeafNode("Text 4", None)
                    ]
                )
            ]
        )
        self.assertEqual(node.to_html(), "<p><p><b>Text 1</b>Text 2</p><i><b>Text 3</b>Text 4</i></p>")

    def test_no_children(self):
        node = ParentNode("p", None)
        with self.assertRaises(ValueError):
            html = node.to_html()

    def test_empty_children(self):
        node = ParentNode("p", [])
        with self.assertRaises(ValueError):
            html = node.to_html()