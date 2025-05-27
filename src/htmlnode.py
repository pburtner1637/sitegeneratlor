class HTMLNode:
    """
    Represents a node in an HTML tree structure.

    Attributes:
        tag (str, optional): The HTML tag name (e.g., "p", "a", "h1"). Defaults to None.
        value (str, optional): The text content of the HTML tag. Defaults to None.
        children (list, optional): A list of HTMLNode objects representing child nodes. Defaults to None.
        props (dict, optional): A dictionary of key-value pairs representing HTML attributes. Defaults to None.
    """
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Raises a NotImplementedError. This method should be overridden by child classes
        to render the node as an HTML string.
        """
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        """
        Converts the 'props' dictionary into an HTML attribute string.

        Returns:
            str: A string representing the HTML attributes (e.g., ' href="url" target="_blank"').
                 Returns an empty string if self.props is None or empty.
        """
        if self.props is None:
            return ""
        
        html_attributes = []
        for key, value in self.props.items():
            html_attributes.append(f'{key}="{value}"')
        
        # Join with a space and add a leading space if there are attributes
        return " " + " ".join(html_attributes) if html_attributes else ""

    def __repr__(self):
        """
        Returns a string representation of the HTMLNode object for debugging.
        Format: HTMLNode(tag, value, children, props)
        """
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

