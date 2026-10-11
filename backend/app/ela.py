import io
import base64
from PIL import Image, ImageChops, ImageEnhance
import numpy as np

def perform_ela(image_data, quality=90, amplification=10):
    """
    Perform Error Level Analysis on JPEG image

    Args:
        image_data: Original image bytes
        quality: JPEG compression quality for re-saving (default 90)
        amplification: Factor to amplify differences for visibility (default 10)

    Returns:
        base64 encoded PNG image of ELA result or None if failed
    """
    try:
        # Open original image
        original_image = Image.open(io.BytesIO(image_data))

        # Convert to RGB if necessary (for consistency)
        if original_image.mode != 'RGB':
            original_image = original_image.convert('RGB')

        # Save original image at specified quality to buffer
        buffer = io.BytesIO()
        original_image.save(buffer, format='JPEG', quality=quality)
        buffer.seek(0)

        # Open the re-saved image
        recompressed_image = Image.open(buffer)

        # Calculate difference
        ela_image = ImageChops.difference(original_image, recompressed_image)

        # Enhance the difference for visibility
        extrema = ela_image.getextrema()
        max_diff = max([ex[1] for ex in extrema])

        if max_diff == 0:
            # No difference found, return a uniform image
            ela_image = Image.new('L', original_image.size, 0)
        else:
            scale = 255.0 / max_diff * amplification
            ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)

        # Convert to RGB for consistent output
        if ela_image.mode != 'RGB':
            ela_image = ela_image.convert('RGB')

        # Save ELA image as PNG to buffer
        ela_buffer = io.BytesIO()
        ela_image.save(ela_buffer, format='PNG')
        ela_buffer.seek(0)

        # Encode as base64
        ela_base64 = base64.b64encode(ela_buffer.getvalue()).decode('utf-8')

        return ela_base64

    except Exception as e:
        # Return None if ELA processing fails
        return None