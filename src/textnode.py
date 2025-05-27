from enum import Enum

class TextType(Enum):
    """
    Represents various types of text nodes or document formats
    that primarily contain text content.
    """
    PLAIN_TEXT = "txt"
    MARKDOWN = "md"
    WORD_DOCUMENT = "docx"
    POWERPOINT_PRESENTATION_X = "pptx"
    POWERPOINT_PRESENTATION = "ppt"
    PDF_DOCUMENT = "pdf"
    CODE = "code" # For text-based code files (e.g., .py, .js)


class TextNode:
    """
    Represents a text node in a document, with content, type, and an optional URL.
    """
    def __init__(self, text, text_type, url=None):
        """
        Initializes a TextNode.

        Args:
            text (str): The text content of the node.
            text_type (TextType): The type of text this node contains (e.g., PLAIN_TEXT, MARKDOWN).
            url (str, optional): The URL of the link or image, if applicable. Defaults to None.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        """
        Compares two TextNode objects for equality.
        Returns True if all properties (text, text_type, url) are equal.
        """
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        """
        Returns a string representation of the TextNode object.
        Format: TextNode(TEXT, TEXT_TYPE, URL)
        """
        return f"TextNode({self.text!r}, {self.text_type!r}, {self.url!r})"

# Example Usage (for testing purposes)
if __name__ == "__main__":
    node1 = TextNode("This is a paragraph", TextType.PLAIN_TEXT)
    node2 = TextNode("This is a link", TextType.MARKDOWN, "https://example.com")
    node3 = TextNode("This is a paragraph", TextType.PLAIN_TEXT)
    node4 = TextNode("This is a different paragraph", TextType.PLAIN_TEXT)
    node5 = TextNode("This is a link", TextType.MARKDOWN, "https://example.com")
    node6 = TextNode("This is a link", TextType.MARKDOWN, "https://another.com")

    print(f"Node 1: {node1}")
    print(f"Node 2: {node2}")

    print(f"\nNode 1 == Node 3: {node1 == node3}") # Expected: True
    print(f"Node 1 == Node 4: {node1 == node4}") # Expected: False
    print(f"Node 2 == Node 5: {node2 == node5}") # Expected: True
    print(f"Node 2 == Node 6: {node2 == node6}") # Expected: False
    print(f"Node 1 == 'some string': {node1 == 'some string'}") # Expected: False (due to NotImplemented)
