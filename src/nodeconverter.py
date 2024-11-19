import re

from textnode import *
from htmlnode import *
from leafnode import *
from parentnode import *

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(text_node.text)
        case TextType.BOLD:
            return LeafNode(text_node.text, "b")
        case TextType.ITALIC:
            return LeafNode(text_node.text, "i")
        case TextType.CODE:
            return LeafNode(text_node.text, "code")
        case TextType.LINK:
            if text_node.url == None:
                raise ValueError("No URL provided.")
            return LeafNode(text_node.text, "a", {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url == None:
                raise ValueError("No image source provided.")
            return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Tag type not recognized.")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        if node.text.count(delimiter) % 2 == 1:
            raise ValueError("Dangling delimiter. (odd count of delimiter)")
        
        if node.text_type == TextType.NORMAL and delimiter in node.text:
            split_text = node.text.split(delimiter)
            for i in range(0, len(split_text)):
                if i % 2 == 0:
                    if len(split_text[i]) > 0:
                        new_nodes.append(TextNode(split_text[i], node.text_type))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))
        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)

        if len(images) > 0:
            remaining_text = node.text
            while len(images) > 0:
                img = images.pop(0)
                split_by_img = remaining_text.split(f"![{img[0]}]({img[1]})", 1)

                if len(split_by_img[0]) > 0:
                    new_nodes.append(TextNode(split_by_img[0], node.text_type))
                new_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
                remaining_text = split_by_img[1]
            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, node.text_type))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        images = extract_markdown_links(node.text)

        if len(images) > 0:
            remaining_text = node.text
            while len(images) > 0:
                img = images.pop(0)
                split_by_img = remaining_text.split(f"[{img[0]}]({img[1]})", 1)

                if len(split_by_img[0]) > 0:
                    new_nodes.append(TextNode(split_by_img[0], node.text_type))
                new_nodes.append(TextNode(img[0], TextType.LINK, img[1]))
                remaining_text = split_by_img[1]
            if len(remaining_text) > 0:
                new_nodes.append(TextNode(remaining_text, node.text_type))
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    trimmed_blocks = []

    for block in blocks:
        trim = block.strip()

        if len(trim) > 0:
            trimmed_blocks.append(trim)

    return trimmed_blocks

def block_to_blocktype(mblock):
    stripped_block = mblock.lstrip()
    if stripped_block[0] == "#" and mblock[len(mblock.split(" ", 1)[0])] == " " and 1 <= len(mblock.split(" ", 1)[0]) <= 6:
        return "heading"
    elif stripped_block[:3] == "```" and mblock[-3:] == "```":
        return "code"
    elif stripped_block[0] == ">":
        return "quote"
    elif (stripped_block[0] == "*" or stripped_block[0] == "-") and stripped_block[1] == " ":
        return "ulist"
    elif stripped_block.split(". ", 1)[0].isnumeric():
        split_by_line = stripped_block.split("\n")
        for i in range(0, len(split_by_line)):
            if int(split_by_line[i].split(". ", 1)[0]) != i + 1:
                return "paragraph"
        return "olist"
    else:
        return "paragraph"
    
def block_to_header(block):
    split_block = block.split(" ", 1)
    nodes = text_to_textnodes(split_block[1])
    children = list(map(text_node_to_html_node, nodes))

    return ParentNode(f"h{split_block[0].count('#')}", children)

def block_to_code(block):
    stripped_block = block.strip("`").strip()
    return ParentNode("pre", [LeafNode(stripped_block, "code")])

def block_to_quote(block):
    stripped_block = block.lstrip(">").strip()
    nodes = text_to_textnodes(stripped_block)
    children = list(map(text_node_to_html_node, nodes))

    return ParentNode("blockquote", children)

def block_to_list(block, ordered = False):
    tag = ""
    
    block_list = []

    if ordered:
        blocks = block.split("\n")
        tag = "ol"
        for b in blocks:
            text = b.split(". ", 1)[1].strip()

            if block_to_blocktype(text) == "paragraph":
                nodes = text_to_textnodes(text)
                if len(nodes) == 1 and nodes[0].text_type == TextType.NORMAL:
                    block_list.append(LeafNode(nodes[0].text, "li"))
                else:
                    html_nodes = list(map(text_node_to_html_node, nodes))
                    block_list.append(ParentNode("li", html_nodes))
            else:
                block_list.append(markdown_to_html_node(text, "li"))
    else:
        bullet = block[0]
        tag = "ul"

        # blocks = block[2:].split(f"\n{bullet} ")
        blocks = re.split(rf"\n\s*{re.escape(bullet)}", block[2:])
        for b in blocks:
            text = b.strip()
            sublists_nested = False

            if "\n" in text:
                sublines = text.split("\n")
                for line in sublines:
                    if block_to_blocktype(line.strip()) == "ulist" or block_to_blocktype(line.strip()) == "olist":
                        sublists_nested = True

            if block_to_blocktype(text) == "paragraph" and sublists_nested:
                sublists = b.split("\n", 1)
                
                ordered = block_to_blocktype(sublists[1].strip()) == "olist"
                nested_list = block_to_list(sublists[1].strip(), ordered)
                
                nodes = text_to_textnodes(sublists[0])
                if len(nodes) == 1 and nodes[0].text_type == TextType.NORMAL:
                    list_label = LeafNode(sublists[0])
                else:
                    html_nodes = list(map(text_node_to_html_node, nodes))
                    list_label = markdown_to_html_node(sublists[0], "")
                block_list.append(ParentNode("li", [list_label, nested_list]))
            elif block_to_blocktype(text) == "paragraph":
                nodes = text_to_textnodes(text)
                if len(nodes) == 1 and nodes[0].text_type == TextType.NORMAL:
                    block_list.append(LeafNode(nodes[0].text, "li"))
                else:
                    html_nodes = list(map(text_node_to_html_node, nodes))
                    block_list.append(ParentNode("li", html_nodes))
            else:
                block_list.append(markdown_to_html_node(text.strip(), "li"))

    return ParentNode(tag, block_list)
    
def markdown_to_html_node(markdown, tag = "html"):
    mblocks = markdown_to_blocks(markdown)
    htmlblocks = []

    for block in mblocks:
        match (block_to_blocktype(block)):
            case "heading":
                htmlblocks.append(block_to_header(block))
            case "code":
                htmlblocks.append(block_to_code(block))
            case "quote":
                htmlblocks.append(block_to_quote(block))
            case "ulist":
                htmlblocks.append(block_to_list(block, False))
            case "olist":
                htmlblocks.append(block_to_list(block, True))
            case "paragraph":
                nodes = list(map(text_node_to_html_node, text_to_textnodes(block)))
                htmlblocks.append(ParentNode("p", nodes))
                # htmlblocks.append(LeafNode(block, "p"))

    return ParentNode(tag, htmlblocks)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)

    if not blocks[0].strip().startswith("# "):
        raise Exception('No title in file (Add header with "# ").')
    
    return blocks[0].strip()[2:]
    
