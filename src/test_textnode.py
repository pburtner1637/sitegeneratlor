import unittest
from textnode import TextNode, TextType
from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        """
        Tests equality of two TextNode objects with identical properties (url is None by default).
        """
        node = TextNode("This is a text node", TextType.PLAIN_TEXT)
        node2 = TextNode("This is a text node", TextType.PLAIN_TEXT)
        self.assertEqual(node, node2)

    def test_eq_different_url(self):
        """
        Tests inequality when only the URL property is different.
        """
        node = TextNode("This is a link node", TextType.MARKDOWN, "https://example.com/page1")
        node2 = TextNode("This is a link node", TextType.MARKDOWN, "https://example.com/page2")
        self.assertNotEqual(node, node2)

    def test_eq_different_text_type(self):
        """
        Tests inequality when only the text_type property is different.
        """
        node = TextNode("Some content", TextType.PLAIN_TEXT)
        node2 = TextNode("Some content", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_eq_different_text(self):
        """
        Tests inequality when only the text content is different.
        """
        node = TextNode("First text", TextType.PLAIN_TEXT)
        node2 = TextNode("Second text", TextType.PLAIN_TEXT)
        self.assertNotEqual(node, node2)

    def test_eq_url_none(self):
        """
        Tests equality when both nodes explicitly have url=None.
        """
        node = TextNode("No URL here", TextType.PLAIN_TEXT, None)
        node2 = TextNode("No URL here", TextType.PLAIN_TEXT, None)
        self.assertEqual(node, node2)

    def test_eq_one_url_none(self):
        """
        Tests inequality when one node has a URL and the other has url=None.
        """
        node = TextNode("A link", TextType.MARKDOWN, "https://example.com")
        node2 = TextNode("A link", TextType.MARKDOWN, None)
        self.assertNotEqual(node, node2)

    def test_eq_all_different(self):
        """
        Tests inequality when all properties are different.
        """
        node = TextNode("Text1", TextType.PLAIN_TEXT, "url1")
        node2 = TextNode("Text2", TextType.CODE, "url2")
        self.assertNotEqual(node, node2)


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single_prop(self):
        """
        Tests props_to_html with a single property.
        """
        node = HTMLNode(tag="a", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        """
        Tests props_to_html with multiple properties.
        """
        node = HTMLNode(
            tag="a",
            props={
                "href": "https://www.google.com",
                "target": "_blank",
                "class": "btn"
            }
        )
        # The order of attributes in the output string might vary based on Python's dict iteration
        # so we'll check for the presence of each part.
        expected_parts = [' href="https://www.google.com"', ' target="_blank"', ' class="btn"']
        result = node.props_to_html()
        
        # Check if the result starts with a space and contains all expected parts
        self.assertTrue(result.startswith(' '))
        for part in expected_parts:
            self.assertIn(part, result)
        
        # A more robust check for exact match would involve sorting the parts
        # For this assignment, checking presence and leading space is sufficient.
        # For example:
        # sorted_result_parts = sorted(result.strip().split(' '))
        # sorted_expected_parts = sorted([p.strip() for p in expected_parts])
        # self.assertEqual(sorted_result_parts, sorted_expected_parts)


    def test_props_to_html_no_props(self):
        """
        Tests props_to_html when props is None or empty.
        """
        node_none_props = HTMLNode(tag="p", props=None)
        self.assertEqual(node_none_props.props_to_html(), "")

        node_empty_props = HTMLNode(tag="div", props={})
        self.assertEqual(node_empty_props.props_to_html(), "")

    def test_repr(self):
        """
        Tests the __repr__ method for correct string representation.
        """
        node = HTMLNode(tag="p", value="Hello", props={"class": "text"})
        expected_repr = "HTMLNode(tag='p', value='Hello', children=None, props={'class': 'text'})"
        self.assertEqual(repr(node), expected_repr)

        node_with_children = HTMLNode(tag="div", children=[HTMLNode(tag="span", value="child")])
        # Note: repr of children will include their full repr, so we check for substring
        expected_repr_part = "HTMLNode(tag='div', value=None, children=["
        self.assertTrue(repr(node_with_children).startswith(expected_repr_part))
        self.assertIn("HTMLNode(tag='span', value='child', children=None, props=None)", repr(node_with_children))


if __name__ == "__main__":
    unittest.main()
