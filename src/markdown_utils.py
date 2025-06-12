import re

def extract_markdown_images(text):
    """
    Extracts markdown image alt text and URLs from a given text.

    Args:
        text (str): The raw markdown text.

    Returns:
        list: A list of tuples, where each tuple contains (alt_text, url).
              Returns an empty list if no images are found.
    """
    # Regex pattern to find markdown images: ![alt_text](url)
    # (.*?) is a non-greedy match for any character
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown link anchor text and URLs from a given text.

    Args:
        text (str): The raw markdown text.

    Returns:
        list: A list of tuples, where each tuple contains (anchor_text, url).
              Returns an empty list if no links are found.
    """
    # Regex pattern to find markdown links: [anchor_text](url)
    # Use a negative lookbehind (?<!!) to ensure it does not start with '!'
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches

