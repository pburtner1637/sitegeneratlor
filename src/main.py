
# hello world

from textnode import TextNode, TextType

def main():
    """
    Creates a TextNode object with dummy values and prints its representation.
    """
    # Create a TextNode object with some dummy values
    dummy_node = TextNode("Hello, Doc2Doc!", TextType.PLAIN_TEXT, "http://dummyurl.com")

    # Print the TextNode object
    print(dummy_node)

if __name__ == "__main__":
    main()
