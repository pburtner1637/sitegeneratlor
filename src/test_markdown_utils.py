import unittest
from markdown_utils import extract_markdown_images, extract_markdown_links # Import the functions to test

class TestMarkdownUtils(unittest.TestCase):
    def test_extract_markdown_images_single(self):
        """
        Tests extraction of a single markdown image.
        """
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        """
        Tests extraction of multiple markdown images in one text.
        """
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_no_images(self):
        """
        Tests extraction when no markdown images are present.
        """
        text = "This is text with no images or links."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_text(self):
        """
        Tests extraction with empty input text.
        """
        text = ""
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_mixed_content(self):
        """
        Tests extraction with mixed content including links, but only images.
        """
        text = "Text with a link [to boot dev](https://www.boot.dev) and an ![image](https://example.com/img.png)."
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)

    def test_extract_markdown_links_single(self):
        """
        Tests extraction of a single markdown link.
        """
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        """
        Tests extraction of multiple markdown links in one text.
        """
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_no_links(self):
        """
        Tests extraction when no markdown links are present.
        """
        text = "This is text with no links or images."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_text(self):
        """
        Tests extraction with empty input text.
        """
        text = ""
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_mixed_content(self):
        """
        Tests extraction with mixed content including images, but only links.
        """
        text = "Text with an ![image](https://example.com/img.png) and a link [to boot dev](https://www.boot.dev)."
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_images_with_special_chars_in_alt(self):
        """
        Tests image extraction with special characters in alt text.
        """
        text = "![Image with !@#$ special chars](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("Image with !@#$ special chars", "https://example.com/img.png")], matches)

    def test_extract_markdown_links_with_special_chars_in_anchor(self):
        """
        Tests link extraction with special characters in anchor text.
        """
        text = "[Link with &*() special chars](https://example.com/link)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Link with &*() special chars", "https://example.com/link")], matches)

