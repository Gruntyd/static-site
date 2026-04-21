import re
from textnode import TextNode, TextType

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        sections = node.text.split(delimiter)

        if len(sections) % 2 == 0:
            raise ValueError("sections are even.")
        for i in range(len(sections)):
            text = sections[i]
            if text == "":
                continue
        
            if i % 2 == 0:
                new_nodes.append(TextNode(text, TextType.TEXT))
            else:
                new_nodes.append(TextNode(text, text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        results = extract_markdown_images(node.text)
        if not results:
            new_nodes.append(node)
            continue

        text_to_split = node.text
        for tuple in results:
            alt, imageURL = tuple
            beforeSplit, text_to_split = text_to_split.split(f"![{alt}]({imageURL})", 1)
            if beforeSplit:
                new_nodes.append(TextNode(beforeSplit, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, imageURL))

        if text_to_split:
            new_nodes.append(TextNode(text_to_split, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        results = extract_markdown_links(node.text)
        if not results:
            new_nodes.append(node)
            continue

        text_to_split = node.text
        for tuple in results:
            text, url = tuple
            beforeSplit, text_to_split = text_to_split.split(f"[{text}]({url})", 1)
            if beforeSplit:
                new_nodes.append(TextNode(beforeSplit, TextType.TEXT))
            new_nodes.append(TextNode(text, TextType.LINK, url))

        if text_to_split:
            new_nodes.append(TextNode(text_to_split, TextType.TEXT))
    return new_nodes


