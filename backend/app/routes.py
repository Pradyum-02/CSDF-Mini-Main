from flask import Blueprint, request, jsonify
import os
import tempfile
import hashlib
from werkzeug.utils import secure_filename
from PIL import Image
import piexif
import numpy as np
from app.forensic import allowed_file
from app.metadata import extract_metadata
from app.hashing import calculate_hashes
from app.ela import perform_ela
from app.reports import generate_report

bp = Blueprint('api', __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'CSDF - Digital Image Forensics Tool',
        'version': '1.0.0'
    }), 200

@bp.route('/analyze', methods=['POST'])
def analyze_image():
    """Main image analysis endpoint"""
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not supported. Please upload JPEG, PNG, TIFF, WebP, or BMP'}), 400

    try:
        # Read file data
        file_data = file.read()

        # Validate file size
        if len(file_data) > 10 * 1024 * 1024:  # 10MB
            return jsonify({'error': 'File size exceeds 10MB limit'}), 400

        # Reset file pointer for PIL
        file.seek(0)

        # Open image with PIL
        try:
            image = Image.open(file)
            image.verify()  # Verify it's a valid image
            file.seek(0)  # Reset again after verify
            image = Image.open(file)
        except Exception as e:
            return jsonify({'error': f'Invalid image file: {str(e)}'}), 400

        # Extract metadata
        metadata = extract_metadata(image, file.filename)

        # Calculate hashes
        hashes = calculate_hashes(file_data)

        # Perform ELA (only for JPEG)
        ela_result = None
        if image.format in ['JPEG', 'JPG']:
            ela_result = perform_ela(file_data)

        # Generate unique analysis ID
        analysis_id = hashlib.md5((file.filename + str(len(file_data))).encode()).hexdigest()[:8]

        # Prepare response
        response = {
            'analysis_id': analysis_id,
            'filename': secure_filename(file.filename),
            'file_size': len(file_data),
            'format': image.format,
            'width': image.width,
            'height': image.height,
            'mode': image.mode,
            'metadata': metadata,
            'hashes': hashes,
            'ela_available': image.format in ['JPEG', 'JPG'],
            'ela_result': ela_result
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@bp.route('/report', methods=['POST'])
def generate_report_endpoint():
    """Generate downloadable report"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    try:
        report_data = generate_report(data)
        format_type = data.get('format', 'txt').lower()

        if format_type == 'json':
            return jsonify(report_data), 200
        else:
            # Generate text report
            text_report = f"""CSDF - Digital Image Forensics Analysis Report
==================================================

Analysis ID: {report_data.get('analysis_id', 'N/A')}
Timestamp: {report_data.get('timestamp', 'N/A')}
Original Filename: {report_data.get('original_filename', 'N/A')}

FILE INFORMATION
----------------
File Size: {report_data.get('file_size', 0)} bytes ({report_data.get('file_size', 0) / 1024:.2f} KB)
Format: {report_data.get('format', 'N/A')}
Dimensions: {report_data.get('width', 0)} x {report_data.get('height', 0)} pixels
Aspect Ratio: {report_data.get('aspect_ratio', 'N/A'):.2f}
Color Mode: {report_data.get('color_mode', 'N/A')}

METADATA INFORMATION
--------------------
"""

            metadata = report_data.get('metadata', {})
            if metadata:
                for key, value in metadata.items():
                    if value and value != 'Not Available':
                        text_report += f"{key}: {value}\n"
            else:
                text_report += "No metadata available\n"

            text_report += f"""
CRYPTOGRAPHIC HASHES
--------------------
MD5:     {report_data.get('hashes', {}).get('md5', 'N/A')}
SHA-1:   {report_data.get('hashes', {}).get('sha1', 'N/A')}
SHA-256: {report_data.get('hashes', {}).get('sha256', 'N/A')}

ELA INFORMATION
---------------
ELA Available: {'Yes' if report_data.get('ela_available') else 'No'}
"""

            if report_data.get('ela_result'):
                text_report += f"ELA Generated: Yes (Quality: 90, Amplification: 10)\n"
            else:
                text_report += "ELA Generated: No (Not applicable for this image format)\n"

            text_report += f"""
ANALYSIS NOTES
--------------
{report_data.get('notes', 'Analysis completed successfully.')}
"""

            return text_report, 200, {
                'Content-Type': 'text/plain',
                'Content-Disposition': f'attachment; filename=csdf_report_{report_data.get("analysis_id", "unknown")}.txt'
            }

    except Exception as e:
        return jsonify({'error': f'Report generation failed: {str(e)}'}), 500