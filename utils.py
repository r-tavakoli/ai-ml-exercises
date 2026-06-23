import re
from typing import Union, List
import numpy as np # linear algebra
import struct
from array import array


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






#
# MNIST Data Loader Class 
# source: https://www.kaggle.com/code/hojjatk/read-mnist-dataset/notebook
#
class MnistDataloader(object):
    def __init__(self, training_images_filepath,training_labels_filepath,
                 test_images_filepath, test_labels_filepath):
        self.training_images_filepath = training_images_filepath
        self.training_labels_filepath = training_labels_filepath
        self.test_images_filepath = test_images_filepath
        self.test_labels_filepath = test_labels_filepath
    
    def read_images_labels(self, images_filepath, labels_filepath):        
        labels = []
        with open(labels_filepath, 'rb') as file:
            magic, size = struct.unpack(">II", file.read(8))
            if magic != 2049:
                raise ValueError('Magic number mismatch, expected 2049, got {}'.format(magic))
            labels = array("B", file.read())        
        
        with open(images_filepath, 'rb') as file:
            magic, size, rows, cols = struct.unpack(">IIII", file.read(16))
            if magic != 2051:
                raise ValueError('Magic number mismatch, expected 2051, got {}'.format(magic))
            image_data = array("B", file.read())        
        images = []
        for i in range(size):
            images.append([0] * rows * cols)
        for i in range(size):
            img = np.array(image_data[i * rows * cols:(i + 1) * rows * cols])
            img = img.reshape(28, 28)
            images[i][:] = img            
        
        return images, labels
            
    def load_data(self):
        x_train, y_train = self.read_images_labels(self.training_images_filepath, self.training_labels_filepath)
        x_test, y_test = self.read_images_labels(self.test_images_filepath, self.test_labels_filepath)
        return (x_train, y_train),(x_test, y_test)      

        