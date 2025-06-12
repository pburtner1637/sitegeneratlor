import re
from enum import Enum # Import Enum

from src.textnode import TextNode, TextType
from src.markdown_utils import extract_markdown_images, extract_markdown_links # Corrected import path for markdown_utils
from src.htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node # Corrected import path for htmlnode


# New BlockType Enum
class BlockType(Enum):
    """
    Represents various types of markdown blocks.
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Splits TextNode objects of TextType.PLAIN_TEXT based on a delimiter,
    creating new TextNode objects with the specified text_type for delimited content.

    Args:
        old_nodes (list): A list of TextNode objects.
        delimiter (str): The string used to delimit content (e.g., '`', '**', '_').
        text_type (TextType): The TextType enum member for the delimited content
                               (e.g., TextType.CODE, TextType.BOLD, TextType.ITALIC).

    Returns:
        list: A new list of TextNode objects after splitting.

    Raises:
        ValueError: If an unclosed delimiter is found.
    """
    new_nodes = []
    for node in old_nodes:
        # If the node is not plain text, it's already formatted, so just add it.
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text_content = node.text
        # If the text content is empty, skip processing and don't add an empty node
        if not text_content:
            continue

        parts = text_content.split(delimiter)

        # Check for unclosed delimiters: The number of parts must be odd
        # (meaning an even number of delimiters, forming pairs).
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown syntax: Unclosed delimiter '{delimiter}' found in '{node.text}'")

        # Process the parts:
        # Even indices are plain text, odd indices are delimited content.
        for i, part in enumerate(parts):
            if part == "": # Skip empty parts that result from ` ` or delimiter at start/end
                continue

            if i % 2 == 0:  # Even index: plain text
                new_nodes.append(TextNode(part, TextType.PLAIN_TEXT))
            else:  # Odd index: delimited content
                new_nodes.append(TextNode(part, text_type))
    return new_nodes


def split_nodes_image(old_nodes):
    """
    Splits TextNode objects of TextType.PLAIN_TEXT based on markdown image syntax,
    creating new TextNode objects for plain text and image nodes.

    Args:
        old_nodes (list): A list of TextNode objects.

    Returns:
        list: A new list of TextNode objects after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        # If the node is not plain text, it's already formatted, so just add it.
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text_content = node.text
        # If the text content is empty, skip processing and don't add an empty node
        if not text_content:
            continue

        # Use re.finditer to get match objects with start/end positions
        matches = list(re.finditer(r"!\[(.*?)\]\((.*?)\)", text_content))

        if not matches:
            # If no images are found in this plain text node, add it as is
            new_nodes.append(node)
            continue

        last_idx = 0
        for match in matches:
            # Add plain text before the current image match
            plain_text_segment = text_content[last_idx:match.start()]
            if plain_text_segment: # Only add if not empty
                new_nodes.append(TextNode(plain_text_segment, TextType.PLAIN_TEXT))
            
            # Add the image node
            alt_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Update last_idx to the end of the current match
            last_idx = match.end()
        
        # Add any remaining plain text after the last image
        remaining_text = text_content[last_idx:]
        if remaining_text: # Only add if not empty
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN_TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Splits TextNode objects of TextType.PLAIN_TEXT based on markdown link syntax,
    creating new TextNode objects for plain text and link nodes.

    Args:
        old_nodes (list): A list of TextNode objects.

    Returns:
        list: A new list of TextNode objects after splitting.
    """
    new_nodes = []
    for node in old_nodes:
        # If the node is not plain text, it's already formatted, so just add it.
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text_content = node.text
        # If the text content is empty, skip processing and don't add an empty node
        if not text_content:
            continue

        # Use re.finditer with negative lookbehind for links
        matches = list(re.finditer(r"(?<!!)\[(.*?)\]\((.*?)\)", text_content))

        if not matches:
            # If no links are found in this plain text node, add it as is
            new_nodes.append(node)
            continue

        last_idx = 0
        for match in matches:
            # Add plain text before the current link match
            plain_text_segment = text_content[last_idx:match.start()]
            if plain_text_segment: # Only add if not empty
                new_nodes.append(TextNode(plain_text_segment, TextType.PLAIN_TEXT))
            
            # Add the link node
            anchor_text = match.group(1)
            url = match.group(2)
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Update last_idx to the end of the current match
            last_idx = match.end()
        
        # Add any remaining plain text after the last link
        remaining_text = text_content[last_idx:]
        if remaining_text: # Only add if not empty
            new_nodes.append(TextNode(remaining_text, TextType.PLAIN_TEXT))
            
    return new_nodes


def text_to_textnodes(text):
    """
    Converts a raw markdown text string into a list of TextNode objects,
    splitting by images, links, and various delimiters (bold, italic, code).

    Args:
        text (str): The raw markdown text.

    Returns:
        list: A list of TextNode objects representing the parsed markdown.
    """
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]
    
    # Process code blocks first
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # Then images and links
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # Then bold and italic
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC) # Corrected delimiter for italic
    
    return nodes

def markdown_to_blocks(markdown):
    """
    Splits a raw Markdown string into a list of "block" strings based on double newlines.
    Strips leading/trailing whitespace and removes empty blocks.

    Args:
        markdown (str): The raw Markdown text representing a full document.

    Returns:
        list: A list of block strings.
    """
    # Split by one or more blank lines (double newlines)
    blocks = markdown.split('\n\n')
    
    cleaned_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block: # Only add non-empty blocks
            cleaned_blocks.append(stripped_block)
            
    return cleaned_blocks


def block_to_block_type(block):
    """
    Determines the type of a markdown block.

    Args:
        block (str): A string representing a markdown block (assumed to have
                     leading/trailing whitespace stripped).

    Returns:
        BlockType: The type of the block (e.g., HEADING, CODE, PARAGRAPH).
    """
    # Heading check
    # Headings start with 1-6 # characters, followed by a space and then the heading text.
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Code block check
    # Must start with 3 backticks and end with 3 backticks.
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Quote block check
    # Every line in a quote block must start with a > character.
    lines = block.split('\n')
    is_quote = True
    for line in lines:
        if not line.startswith(">"):
            is_quote = False
            break
    if is_quote:
        return BlockType.QUOTE

    # Unordered list check
    # Every line in an unordered list block must start with a - or * character, followed by a space.
    is_unordered_list = True
    for line in lines:
        if not (line.startswith("- ") or line.startswith("* ")):
            is_unordered_list = False
            break
    if is_unordered_list:
        return BlockType.UNORDERED_LIST

    # Ordered list check
    # Every line in an ordered list block must start with a number followed by a '.' and a space.
    # The number must start at 1 and increment by 1 for each line.
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    # If none of the above conditions are met, the block is a normal paragraph.
    return BlockType.PARAGRAPH


def text_to_children(text):
    """
    Converts raw text with inline markdown into a list of HTMLNode children.
    This acts as a bridge from TextNodes to HTMLNodes after inline parsing.

    Args:
        text (str): The raw text content of a block (after block-level parsing).

    Returns:
        list: A list of HTMLNode objects representing the inline markdown.
    """
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


def convert_list_items(block, is_ordered):
    """
    Helper function to convert list block lines into a list of HTML li nodes.
    """
    lines = block.split('\n')
    list_items = []
    for line in lines:
        content = ""
        if is_ordered:
            # For ordered lists, skip the number and dot (e.g., "1. ")
            parts = line.split('. ', 1) # Split only on the first occurrence
            if len(parts) > 1:
                content = parts[1]
            else:
                content = line # Fallback for malformed lines, though block_to_block_type should prevent
        else: # Unordered list
            # Skip the "- " or "* " prefix
            content = line[2:]
        
        # Convert the content of the list item (which might have inline markdown)
        item_children = text_to_children(content)
        list_items.append(ParentNode("li", item_children))
    return list_items


def block_to_html_node(block):
    """
    Converts a single markdown block string into an HTMLNode.

    Args:
        block (str): A string representing a markdown block.

    Returns:
        HTMLNode: The corresponding HTMLNode object for the block.

    Raises:
        ValueError: If an unknown block type is encountered.
    """
    block_type = block_to_block_type(block)

    if block_type == BlockType.PARAGRAPH:
        children = text_to_children(block.replace('\n', ' ')) # Replace newlines with spaces for paragraph
        return ParentNode("p", children)
    elif block_type == BlockType.HEADING:
        level = 0
        for char in block:
            if char == '#':
                level += 1
            else:
                break
        heading_text = block[level:].strip() # Remove hashes and leading space
        children = text_to_children(heading_text)
        return ParentNode(f"h{level}", children)
    elif block_type == BlockType.CODE:
        # Code blocks: remove triple backticks from start and end, and strip only leading newline
        # This preserves trailing newlines within the code block content.
        code_content = block[3:-3].lstrip('\n')
        code_node = LeafNode("code", code_content)
        return ParentNode("pre", [code_node])
    elif block_type == BlockType.QUOTE:
        # Remove leading '>' and space from each line
        lines = block.split('\n')
        cleaned_lines = [line[1:].strip() for line in lines]
        quote_text = "\n".join(cleaned_lines) # Rejoin with newlines if multi-line
        children = text_to_children(quote_text)
        return ParentNode("blockquote", children)
    elif block_type == BlockType.UNORDERED_LIST:
        list_items_nodes = convert_list_items(block, False)
        return ParentNode("ul", list_items_nodes)
    elif block_type == BlockType.ORDERED_LIST:
        list_items_nodes = convert_list_items(block, True)
        return ParentNode("ol", list_items_nodes)
    else:
        raise ValueError(f"Unknown block type encountered: {block_type}")


def markdown_to_html_node(markdown):
    """
    Converts a full markdown document into a single parent HTMLNode.

    Args:
        markdown (str): The raw markdown document string.

    Returns:
        ParentNode: A div HTMLNode containing child HTMLNodes for each block.
    """
    blocks = markdown_to_blocks(markdown)
    block_html_nodes = []
    for block in blocks:
        if block: # Ensure block is not empty after stripping
            html_node = block_to_html_node(block)
            block_html_nodes.append(html_node)
    
    return ParentNode("div", block_html_nodes)

def extract_title(markdown):
    """
    Extracts the H1 header from a markdown string.

    Args:
        markdown (str): The full markdown content.

    Returns:
        str: The extracted H1 title.

    Raises:
        Exception: If no H1 header is found.
    """
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No H1 header found in markdown.")

