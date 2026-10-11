import pytest
import io
from PIL import Image
from app.forensic import allowed_file

def test_allowed_file():
    """Test file extension validation"""
    # Test allowed extensions
    assert allowed_file('test.jpg') == True
    assert allowed_file('test.jpeg') == True
    assert allowed_file('test.png') == True
    assert allowed_file('test.tiff') == True
    assert allowed_file('test.bmp') == True
    assert allowed_file('test.webp') == True

    # Test case insensitivity
    assert allowed_file('test.JPG') == True
    assert allowed_file('test.PNG') == True

    # Test disallowed extensions
    assert allowed_file('test.txt') == False
    assert allowed_file('test.exe') == False
    assert allowed_file('test.pdf') == False
    assert allowed_file('test') == False  # No extension

def test_allowed_file_edge_cases():
    """Test edge cases for file validation"""
    assert allowed_file('.hidden.jpg') == True  # Hidden file with extension
    assert allowed_file('test.') == False  # Empty extension
    assert allowed_file('test..jpg') == True  # Double dot