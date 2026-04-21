from enum import Enum
import re

from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import ParentNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING

    lines = block.split("\n")
    if lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    i = 1
    if block.startswith(f"{i}. "):
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            cleaned.append(stripped)
    return cleaned

def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(ParentNode("p", text_to_children(block)))
        elif block_type == BlockType.HEADING:
            level = len(block.split(" ", 1)[0])
            text = block.split(" ", 1)[1]
            tag = "h" + str(level)
            children.append(ParentNode(tag, text_to_children(text)))
        elif block_type == BlockType.CODE:
            text = block[3:-3].strip()
            code_node = text_node_to_html_node(TextNode(text, TextType.TEXT))
            children.append(ParentNode("pre", [ParentNode("code", [code_node])]))
        elif block_type == BlockType.QUOTE:
            blocks = block.split("\n")
            cleaned = []
            for line in blocks:
                stripped = line.lstrip("> ")
                cleaned.append(stripped)
            children.append(ParentNode("blockquote", text_to_children(" ".join(cleaned))))
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                text = line.lstrip("- ")
                li_nodes.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ul", li_nodes))
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            li_nodes = []
            for line in lines:
                text = line.split(" ", 1)[1]
                li_nodes.append(ParentNode("li", text_to_children(text)))
            children.append(ParentNode("ol", li_nodes))
    return ParentNode("div", children)