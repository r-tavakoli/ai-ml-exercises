import re
from typing import Union, List


def _convert_text_to_snake_case(text: str, preserve_underscores: bool) -> str:
    """Helper function to convert a single string to snake_case."""

    # Remove whitespace from ends
    text = text.strip()
    
    if preserve_underscores:
        # Handle underscores specially: replace non-alnum with space
        text = re.sub(r'[^a-zA-Z0-9_]', ' ', text)
        # Insert underscores between word boundaries
        text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
        # Convert to lowercase and normalize spaces
        text = text.lower()
        text = re.sub(r'\s+', '_', text)
        # Clean up multiple underscores
        text = re.sub(r'_+', '_', text)
        return text
    else:
        # Replace all non-alphanumeric with space
        text = re.sub(r'[^a-zA-Z0-9]', ' ', text)
        # Insert underscores between word boundaries
        text = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)
        text = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', text)
        # Convert to lowercase and normalize spaces
        text = text.lower()
        text = re.sub(r'\s+', '_', text)
        # Clean up multiple underscores
        text = re.sub(r'_+', '_', text)
        return text

def to_snake_case(value: Union[str, List[str]], preserve_underscores: bool = False) -> Union[str, List[str]]:
    """
    Convert any string or list of strings to snake_case with additional options.
    
    Args:
        text: The string or list of strings to convert
        preserve_underscores: If True, existing underscores are kept as separators
    
    Examples:
        >>> to_snake_case("  Hello   World  ")
        'hello_world'
        >>> to_snake_case(["Hello World", "getHTTPResponse"])
        ['hello_world', 'get_http_response']
        >>> to_snake_case("getHTTPResponse")
        'get_http_response'
        >>> to_snake_case("__init__")
        '__init__'
        >>> to_snake_case("  __init__  ")
        '__init__'
        >>> to_snake_case("MyClass123")
        'my_class123'
        >>> to_snake_case("  MyClass123  ")
        'my_class123'
    """

    # Handle list input
    if isinstance(value, list):
        return {item: _convert_text_to_snake_case(item, preserve_underscores) for item in value}
    
    if not value or not isinstance(value, str):
        return ''
        
    return {value: _convert_text_to_snake_case(value, preserve_underscores)}
        