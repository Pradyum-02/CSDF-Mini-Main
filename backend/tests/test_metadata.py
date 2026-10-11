import pytest
from PIL import Image
import io
from app.metadata import extract_metadata

def test_extract_metadata_basic():
    """Test metadata extraction from basic image"""
    # Create a simple test image
    img = Image.new('RGB', (100, 100), color='red')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    img = Image.open(img_byte_arr)

    metadata = extract_metadata(img, "test.png")

    assert metadata['Format'] == 'PNG'
    assert metadata['Width'] == 100
    assert metadata['Height'] == 100
    assert metadata['Color Mode'] == 'RGB'
    assert metadata['Aspect Ratio'] == 1.0

def test_extract_metadata_no_exif():
    """Test metadata extraction from image without EXIF"""
    img = Image.new('RGB', (50, 75), color='blue')
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    img = Image.open(img_byte_arr)

    metadata = extract_metadata(img, "no_exif.png")

    assert metadata['Format'] == 'PNG'
    assert metadata['Width'] == 50
    assert metadata['Height'] == 75
    # Should indicate no EXIF data found
    assert 'Note' in metadata or len([k for k in metadata.keys() if k not in ['Format', 'Width', 'Height', 'Aspect Ratio', 'Color Mode']]) == 0