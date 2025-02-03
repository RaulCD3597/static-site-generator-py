import re
from typing import List, Tuple

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    result = []
    for node in old_nodes:
        chunks = node.text.split(delimiter)
        for i, chunk in enumerate(chunks):
            if chunk == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(chunk, node.text_type))
            else:
                result.append(TextNode(chunk, text_type))
    return result


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]+)\]\(([^\(\)]+)\)", text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)", text)


def split_nodes_image(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        text_to_split = node.text
        for alt, url in matches:
            splits = text_to_split.split(f"![{alt}]({url})", 1)
            for split in filter(lambda x: x != "", splits[:-1]):
                new_nodes.append(TextNode(split, node.text_type))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            text_to_split = splits[-1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, node.text_type))
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
            continue
        text_to_split = node.text
        for text, url in matches:
            splits = text_to_split.split(f"[{text}]({url})", 1)
            for split in filter(lambda x: x != "", splits[:-1]):
                new_nodes.append(TextNode(split, node.text_type))
            new_nodes.append(TextNode(text, TextType.LINK, url))
            text_to_split = splits[-1]
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, node.text_type))
    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "*", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
