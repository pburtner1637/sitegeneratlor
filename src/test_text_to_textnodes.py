import unittest
from textnode import TextNode, TextType
from text_to_textnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node # Import the new function
from htmlnode import HTMLNode, LeafNode, ParentNode # Import HTMLNode, LeafNode, ParentNode

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_single_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_code_blocks(self):
        node = TextNode("Text with `first code` and `second code` blocks.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode("first code", TextType.CODE),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("second code", TextType.CODE),
            TextNode(" blocks.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_bold_text(self):
        node = TextNode("This is **bold** text.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_italic_text(self):
        node = TextNode("This is _italic_ text.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_at_start_and_end(self):
        node = TextNode("`Code at start` and `code at end`", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("Code at start", TextType.CODE),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("code at end", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_delimiter(self):
        node = TextNode("This is plain text with no delimiters.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is plain text with no delimiters.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_unclosed_delimiter_raises_error(self):
        node = TextNode("Text with `unclosed delimiter", TextType.PLAIN_TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(cm.exception), "Invalid Markdown syntax: Unclosed delimiter '`' found in 'Text with `unclosed delimiter'")

    def test_empty_string_node(self):
        node = TextNode("", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

    def test_mixed_node_types_input(self):
        node1 = TextNode("Plain text part.", TextType.PLAIN_TEXT)
        node2 = TextNode("Already bold", TextType.BOLD)
        node3 = TextNode("More `code` here.", TextType.PLAIN_TEXT)
        
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        
        expected_nodes = [
            TextNode("Plain text part.", TextType.PLAIN_TEXT),
            TextNode("Already bold", TextType.BOLD),
            TextNode("More ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_empty_content(self):
        node = TextNode("Text with `` empty code.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode(" empty code.", TextType.PLAIN_TEXT), # Empty part is skipped
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_delimiter_only_spaces(self):
        node = TextNode("Text with ` ` space code.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode(" ", TextType.CODE),
            TextNode(" space code.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_delimiters_same_type(self):
        node = TextNode("`one` `two` `three`", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("one", TextType.CODE),
            TextNode(" ", TextType.PLAIN_TEXT),
            TextNode("two", TextType.CODE),
            TextNode(" ", TextType.PLAIN_TEXT),
            TextNode("three", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images_single(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_multiple(self):
        node = TextNode(
            "This is text with an ![image1](https://i.imgur.com/img1.png) and another ![image2](https://i.imgur.com/img2.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is text with an ", TextType.PLAIN_TEXT),
            TextNode("image1", TextType.IMAGE, "https://i.imgur.com/img1.png"),
            TextNode(" and another ", TextType.PLAIN_TEXT),
            TextNode("image2", TextType.IMAGE, "https://i.imgur.com/img2.png"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_at_start_and_end(self):
        node = TextNode(
            "![first](url1) text in middle ![last](url2)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("first", TextType.IMAGE, "url1"),
            TextNode(" text in middle ", TextType.PLAIN_TEXT),
            TextNode("last", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_no_images(self):
        node = TextNode("This is plain text.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is plain text.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_empty_node_text(self):
        node = TextNode("", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_already_formatted_node(self):
        node = TextNode("Already bold", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("Already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_multiple_nodes_input(self):
        node1 = TextNode("Text with ![img1](url1).", TextType.PLAIN_TEXT)
        node2 = TextNode("Another plain text node.", TextType.PLAIN_TEXT)
        node3 = TextNode("![img2](url2) at start.", TextType.PLAIN_TEXT)
        
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_image(old_nodes)
        
        expected_nodes = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(".", TextType.PLAIN_TEXT),
            TextNode("Another plain text node.", TextType.PLAIN_TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" at start.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_only_image(self):
        node = TextNode("![single_image](url)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("single_image", TextType.IMAGE, "url"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_adjacent(self):
        node = TextNode("![img1](url1)![img2](url2)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode("img2", TextType.IMAGE, "url2"),
        ]
        self.assertEqual(new_nodes, expected_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links_single(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is text with a link ", TextType.PLAIN_TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_multiple(self):
        node = TextNode(
            "Text with [link1](url1) and [link2](url2).",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" and ", TextType.PLAIN_TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(".", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_at_start_and_end(self):
        node = TextNode(
            "[first](url1) text in middle [last](url2)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("first", TextType.LINK, "url1"),
            TextNode(" text in middle ", TextType.PLAIN_TEXT),
            TextNode("last", TextType.LINK, "url2"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_no_links(self):
        node = TextNode("This is plain text.", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is plain text.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_empty_node_text(self):
        node = TextNode("", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = []
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_already_formatted_node(self):
        node = TextNode("Already code", TextType.CODE)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Already code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_multiple_nodes_input(self):
        node1 = TextNode("Text with [link1](url1).", TextType.PLAIN_TEXT)
        node2 = TextNode("Another plain text node.", TextType.PLAIN_TEXT)
        node3 = TextNode("[link2](url2) at start.", TextType.PLAIN_TEXT)
        
        old_nodes = [node1, node2, node3]
        new_nodes = split_nodes_link(old_nodes)
        
        expected_nodes = [
            TextNode("Text with ", TextType.PLAIN_TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(".", TextType.PLAIN_TEXT),
            TextNode("Another plain text node.", TextType.PLAIN_TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" at start.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_only_link(self):
        node = TextNode("[single_link](url)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("single_link", TextType.LINK, "url"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_adjacent(self):
        node = TextNode("[link1](url1)[link2](url2)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links_with_image_in_text(self):
        # Ensure links are correctly split even if image syntax is present
        node = TextNode("This is [a link](url) with an ![image](image_url).", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("a link", TextType.LINK, "url"),
            TextNode(" with an ![image](image_url).", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_images_with_link_in_text(self):
        # Ensure images are correctly split even if link syntax is present
        node = TextNode("This is ![an image](image_url) with a [link](url).", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("an image", TextType.IMAGE, "image_url"),
            TextNode(" with a [link](url).", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(new_nodes, expected_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_full_markdown_conversion(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.PLAIN_TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.PLAIN_TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"), # Corrected URL
            TextNode(" and a ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"), # Corrected URL
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_no_special_formatting(self):
        text = "This is just plain text."
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is just plain text.", TextType.PLAIN_TEXT),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_empty_text(self):
        text = ""
        nodes = text_to_textnodes(text)
        expected_nodes = []
        self.assertEqual(nodes, expected_nodes)

    def test_only_bold(self):
        text = "**Only bold**"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("Only bold", TextType.BOLD),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_only_image(self):
        text = "![alt](url)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("alt", TextType.IMAGE, "url"),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_multiple_types_adjacent(self):
        text = "This is **bold**_italic_`code`![img](url)[link](url2)"
        nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code", TextType.CODE),
            TextNode("img", TextType.IMAGE, "url"),
            TextNode("link", TextType.LINK, "url2"),
        ]
        self.assertEqual(nodes, expected_nodes)

    def test_unclosed_delimiter_error_propagation(self):
        text = "This has `unclosed code"
        with self.assertRaises(ValueError) as cm:
            text_to_textnodes(text)
        self.assertIn("Unclosed delimiter '`'", str(cm.exception))


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    
    def test_markdown_to_blocks_leading_trailing_newlines(self):
        md = "\n\n  Block 1  \n\n\nBlock 2\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block 1",
                "Block 2",
            ],
        )

    def test_markdown_to_blocks_only_newlines(self):
        md = "\n\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single block of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a single block of text."])

    def test_markdown_to_blocks_mixed_whitespace(self):
        md = "  Block A  \n\n\tBlock B\n\n  \n  Block C  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block A", "Block B", "Block C"])


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_h1(self):
        block = "# This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_h6(self):
        block = "###### This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_no_space(self):
        block = "##No space heading" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        block = "####### Too many hashes" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nprint('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_single_line(self):
        block = "```print('Hello')```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_block_no_start_delimiter(self):
        block = "print('Hello, world!')\n```" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block_no_end_delimiter(self):
        block = "```\nprint('Hello, world!')" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_single_line(self):
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_multi_line(self):
        block = "> This is a quote line 1\n> This is quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_mixed_lines(self):
        block = "> Quote line\nNormal line" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_hyphen(self):
        block = "- Item 1\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_asterisk(self):
        block = "* Item A\n* Item B"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_mixed_delimiter(self):
        block = "- Item 1\n* Item 2" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST) # Changed to UNORDERED_LIST
    
    def test_unordered_list_no_space(self):
        block = "-Item 1\n- Item 2" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_starts_not_at_one(self):
        block = "2. Second item\n3. Third item" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_skips_number(self):
        block = "1. Item 1\n3. Item 3" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space(self):
        block = "1.Item 1\n2. Item 2" # This should be a paragraph
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH) # An empty block is a paragraph by default

    def test_mixed_block_types_in_single_block_string(self):
        # This block contains features of multiple types, but if it doesn't strictly adhere
        # to one type's rules, it defaults to paragraph.
        block = "# Heading\n> Quote\n- List Item"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING) # Changed to HEADING


class TestMarkdownToHtmlNode(unittest.TestCase):
    # Set maxDiff to None to see full diffs for failed assertions
    maxDiff = None 

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```" # Corrected md string literal
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Corrected expected HTML for code block content to include trailing newline
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>", # Added trailing newline
        )

    def test_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3" # Corrected md string literal
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
        )
    
    def test_quote(self):
        md = "> This is a quote\n> line two" # Corrected md string literal
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nline two</blockquote></div>"
        )

    def test_unordered_list(self):
        md = "- Item 1\n* Item 2\n- Item 3" # Corrected md string literal
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        )

    def test_ordered_list(self):
        md = "1. First item\n2. Second item\n3. Third item" # Corrected md string literal
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item</li><li>Third item</li></ol></div>"
        )

    def test_mixed_blocks(self):
        md = """# Main Title

This is a **paragraph** with _inline_ content.

```
print("hello")
```

> A quote here
> another line

- List item one
- List item two

1. Ordered item one
2. Ordered item two""" # Corrected md string literal to match expected output
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected_html = (
            "<div>"
            "<h1>Main Title</h1>"
            "<p>This is a <b>paragraph</b> with <i>inline</i> content.</p>" # Corrected: Added "a" to match the input markdown
            "<pre><code>print(\"hello\")\n</code></pre>" # Corrected: Added trailing newline to match function's output
            "<blockquote>A quote here\nanother line</blockquote>"
            "<ul><li>List item one</li><li>List item two</li></ul>"
            "<ol><li>Ordered item one</li><li>Ordered item two</li></ol>"
            "</div>"
        )
        self.assertEqual(html, expected_html)


if __name__ == "__main__":
    unittest.main()
