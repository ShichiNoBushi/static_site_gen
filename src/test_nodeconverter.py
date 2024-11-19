import unittest

from nodeconverter import *

class TestNodeConverter(unittest.TestCase):
    def test_normal_text(self):
        tnode = TextNode("Normal text.", TextType.NORMAL)
        self.assertEqual(str(text_node_to_html_node(tnode)), "HTMLNode(None, Normal text., no children, no props)")

    def test_bold_text(self):
        tnode = TextNode("Bold text.", TextType.BOLD)
        self.assertEqual(str(text_node_to_html_node(tnode)), "HTMLNode(b, Bold text., no children, no props)")

    def test_link_text(self):
        tnode = TextNode("Google.", TextType.LINK, "www.google.com")
        self.assertEqual(str(text_node_to_html_node(tnode)), "HTMLNode(a, Google., no children, {href: www.google.com})")

    def test_image_text(self):
        tnode = TextNode("Funny image.", TextType.IMAGE, "funny_image.gif")
        self.assertEqual(str(text_node_to_html_node(tnode)), "HTMLNode(img, , no children, {src: funny_image.gif, alt: Funny image.})")

    def test_no_url(self):
        tnode = TextNode("Not a site.", TextType.LINK)
        with self.assertRaises(ValueError):
            htmlnode = text_node_to_html_node(tnode)

    def test_unknown_type(self):
        tnode = TextNode("Bullet list.", TextType.BULLET)
        with self.assertRaises(ValueError):
            htmlnode = text_node_to_html_node(tnode)

    def test_nbn(self):
        node_list = [TextNode("This is text with a **bolded phrase** in the middle", TextType.NORMAL)]
        self.assertEqual(str(split_nodes_delimiter(node_list, "**", TextType.BOLD)), "[TextNode(This is text with a , normal, None), TextNode(bolded phrase, bold, None), TextNode( in the middle, normal, None)]")

    def test_in(self):
        node_list = [TextNode("*Italic text* at the beginning.", TextType.NORMAL)]
        self.assertEqual(str(split_nodes_delimiter(node_list, "*", TextType.ITALIC)), "[TextNode(Italic text, italic, None), TextNode( at the beginning., normal, None)]")

    def test_ncnc(self):
        node_list = [TextNode("normal `code` normal `code`", TextType.NORMAL)]
        self.assertEqual(str(split_nodes_delimiter(node_list, "`", TextType.CODE)), "[TextNode(normal , normal, None), TextNode(code, code, None), TextNode( normal , normal, None), TextNode(code, code, None)]")

    def test_justbold(self):
        node_list = [TextNode("**This entire text is bold.**", TextType.NORMAL)]
        self.assertEqual(str(split_nodes_delimiter(node_list, "**", TextType.BOLD)), "[TextNode(This entire text is bold., bold, None)]")

    def test_nobold(self):
        node_list = [TextNode("There is no bold text here.", TextType.NORMAL)]
        self.assertEqual(str(split_nodes_delimiter(node_list, "**", TextType.BOLD)), "[TextNode(There is no bold text here., normal, None)]")

    def test_link(self):
        node_list = [TextNode("**Google**.com", TextType.LINK, "www.google.com")]
        self.assertEqual(str(split_nodes_delimiter(node_list, "**", TextType.BOLD)), "[TextNode(**Google**.com, link, www.google.com)]")

    def test_error_dangle(self):
        node_list = [TextNode("The text is **bold but trails off.", TextType.NORMAL)]
        with self.assertRaises(ValueError):
            new_list = split_nodes_delimiter(node_list, "**", TextType.BOLD)

    def test_extract_image(self):
        images = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertEqual(str(images), "[('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')]")

    def test_extract_noimage(self):
        images = extract_markdown_images("There are no images in this text.")
        self.assertEqual(str(images), "[]")

    def test_extract_link(self):
        links = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertEqual(str(links), "[('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]")

    def test_extract_nolinks(self):
        links = extract_markdown_links("There are no links in this text.")
        self.assertEqual(str(links), "[]")

    def test_split_images(self):
        node = TextNode(
            "Text with ![happy face](smiley.gif)a happy face.",
            TextType.NORMAL
        )
        self.assertEqual(str(split_nodes_image([node])), "[TextNode(Text with , normal, None), TextNode(happy face, image, smiley.gif), TextNode(a happy face., normal, None)]")

    def test_split_2images(self):
        node = TextNode(
            "Happy face![happy face](smily.gif), angry face![mad face](angry.gif).",
            TextType.NORMAL
        )
        self.assertEqual(str(split_nodes_image([node])), "[TextNode(Happy face, normal, None), TextNode(happy face, image, smily.gif), TextNode(, angry face, normal, None), TextNode(mad face, image, angry.gif), TextNode(., normal, None)]")

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.NORMAL,
        )
        self.assertEqual(str(split_nodes_link([node])), "[TextNode(This is text with a link , normal, None), TextNode(to boot dev, link, https://www.boot.dev), TextNode( and , normal, None), TextNode(to youtube, link, https://www.youtube.com/@bootdotdev)]")

    def test_split_noimageslinks(self):
        nodes = [TextNode("No images nor links.", TextType.NORMAL)]
        nodes = split_nodes_link(split_nodes_image(nodes))
        self.assertEqual(str(nodes), "[TextNode(No images nor links., normal, None)]")

    def test_text_convert(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(str(nodes), "[TextNode(This is , normal, None), TextNode(text, bold, None), TextNode( with an , normal, None), TextNode(italic, italic, None), TextNode( word and a , normal, None), TextNode(code block, code, None), TextNode( and an , normal, None), TextNode(obi wan image, image, https://i.imgur.com/fJRm4Vk.jpeg), TextNode( and a , normal, None), TextNode(link, link, https://boot.dev)]")

    def test_text_convert_normal(self):
        text = "This is ordinary text."
        nodes = text_to_textnodes(text)
        self.assertEqual(str(nodes), "[TextNode(This is ordinary text., normal, None)]")

    def test_text_convert_error(self):
        text = "Improperly formatted *text."
        with self.assertRaises(ValueError):
            nodes = text_to_textnodes(text)

    def test_markdown_split(self):
        text = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_markdown_blanklines(self):
        text = """# Header


Paragraph with extra spaces



* List item"""

        expected = [
            "# Header",
            "Paragraph with extra spaces",
            "* List item"
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_markdown_singleline(self):
        text = "Single block no breaks"

        expected = ["Single block no breaks"]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_markdown_whitespace(self):
        text = """   # Header with space   

 * List with indentation
 * Another indented item    """
        
        expected = [
            "# Header with space",
            "* List with indentation\n * Another indented item"
        ]
        self.assertEqual(markdown_to_blocks(text), expected)

    def test_blocktype_h1(self):
        mblock = "# Heading Level 1"
        self.assertEqual(block_to_blocktype(mblock), "heading")

    def test_blocktype_h6(self):
        mblock = "###### Heading level 6"
        self.assertEqual(block_to_blocktype(mblock), "heading")

    def test_blocktype_h7(self):
        mblock = "####### Heading level 7"
        self.assertEqual(block_to_blocktype(mblock), "paragraph")

    def test_blocktype_hnospace(self):
        mblock = "#Heading level 1"
        self.assertEqual(block_to_blocktype(mblock), "paragraph")

    def test_blocktype_code(self):
        mblock = "```print('Hello world!')```"
        self.assertEqual(block_to_blocktype(mblock), "code")

    def test_bloctype_quote(self):
        mblock = "> This is a quote.\n> Each line starts with a '>' character."
        self.assertEqual(block_to_blocktype(mblock), "quote")

    def test_blocktype_uliststar(self):
        mblock = "* Item 1\n* Item 2"
        self.assertEqual(block_to_blocktype(mblock), "ulist")

    def test_blocktype_ulistdash(self):
        mblock = "- Item A\n- Item B"
        self.assertEqual(block_to_blocktype(mblock), "ulist")

    def test_blocktype_ulistnot(self):
        mblock = "*Item 1"
        self.assertEqual(block_to_blocktype(mblock), "paragraph")

    def test_blocktype_olist(self):
        mblock = "1. First item\n2. Second item"
        self.assertEqual(block_to_blocktype(mblock), "olist")

    def test_blocktype_olistnod(self):
        mblock = "A. First item"
        self.assertEqual(block_to_blocktype(mblock), "paragraph")

    def test_html_convert_paragraph(self):
        markdown = "This is a simple paragraph to test."
        expected = "<html><p>This is a simple paragraph to test.</p></html>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected)

    def test_html_convert_header(self):
        markdown = "# Heading 1\nThis is a paragraph following a heading."
        expected = "<html><h1>Heading 1\nThis is a paragraph following a heading.</h1></html>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected)

    def test_html_convert_nested_list(self):
        markdown = "- Item 1\n  * Nested item 1\n  * Nested item 2\n- Item 2"
        expected = "<html><ul><li>Item 1<ul><li>Nested item 1</li><li>Nested item 2</li></ul></li><li>Item 2</li></ul></html>"
        self.assertEqual(markdown_to_html_node(markdown).to_html(), expected)

    def test_extract_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_h3title(self):
        markdown = "*** Header 3"
        with self.assertRaises(Exception):
            title = extract_title(markdown)

    def test_extract_notitle(self):
        markdown = "No title"
        with self.assertRaises(Exception):
            title = extract_title(markdown)