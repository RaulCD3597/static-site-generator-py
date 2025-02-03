from typing import List

from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_OLIST = "ordered_list"
BLOCK_TYPE_ULIST = "unordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = map(lambda x: x.strip(), markdown.split("\n\n"))
    return list(filter(lambda x: x != "", blocks))


def block_to_block_type(block: str) -> str:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BLOCK_TYPE_HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BLOCK_TYPE_CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_QUOTE
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_ULIST
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BLOCK_TYPE_PARAGRAPH
        return BLOCK_TYPE_ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BLOCK_TYPE_PARAGRAPH
            i += 1
        return BLOCK_TYPE_OLIST
    return BLOCK_TYPE_PARAGRAPH


def markdown_to_html_node(markdown: str) -> HTMLNode:
    text_blocks = markdown_to_blocks(markdown)
    children = []
    for block in text_blocks:
        html_node = block_to_htmlnode(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_htmlnode(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BLOCK_TYPE_PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BLOCK_TYPE_HEADING:
        return heading_to_html_node(block)
    if block_type == BLOCK_TYPE_CODE:
        return code_to_html_node(block)
    if block_type == BLOCK_TYPE_OLIST:
        return olist_to_html_node(block)
    if block_type == BLOCK_TYPE_ULIST:
        return ulist_to_html_node(block)
    if block_type == BLOCK_TYPE_QUOTE:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")


def text_to_children(text: str) -> List[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> HTMLNode:
    count = 0
    while block[count] == "#":
        count += 1
    if count + 1 >= len(block):
        raise ValueError(f"Invalid heading level: {count}")
    text = block[count + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{count}", children)


def code_to_html_node(block: str) -> HTMLNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> HTMLNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
