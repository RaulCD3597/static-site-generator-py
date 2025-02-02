from typing import List

BLOCK_TYPE_PARAGRAPH = "paragraph"
BLOCK_TYPE_HEADING = "heading"
BLOCK_TYPE_CODE = "code"
BLOCK_TYPE_QUOTE = "quote"
BLOCK_TYPE_OLIST = "ordered_list"
BLOCK_TYPE_ULIST = "unordered_list"


def markdown_to_blocks(markdown: str) -> List[str]:
    blocks = map(lambda x: x.strip(), markdown.split("\n\n"))
    return list(filter(lambda x: x != "", blocks))


def block_to_block_type(block):
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
