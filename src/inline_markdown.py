from re import findall
from typing import List, Tuple

from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
) -> List[TextNode]:
    result = []
    for node in old_nodes:
        chunks = node.text.split(delimiter)
        if len(chunks) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i, chunk in enumerate(chunks):
            if chunk == "":
                continue
            if i % 2 == 0:
                result.append(TextNode(chunk, node.text_type))
            else:
                result.append(TextNode(chunk, text_type))
    return result


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    return findall(r"!\[([^\[\]]+)\]\(([^\(\)]+)\)", text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    return findall(r"(?<!!)\[([^\[\]]+)\]\(([^\(\)]+)\)", text)
