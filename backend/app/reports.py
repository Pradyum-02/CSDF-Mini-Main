from datetime import datetime
import hashlib

def generate_report(data):
    """Generate report data structure"""
    analysis_id = data.get('analysis_id', 'unknown')
    timestamp = data.get('timestamp', datetime.utcnow().isoformat() + 'Z')

    # Format file size for display
    file_size = data.get('file_size', 0)
    if file_size < 1024:
        size_str = f"{file_size} bytes"
    elif file_size < 1024 * 1024:
        size_str = f"{file_size / 1024:.2f} KB"
    else:
        size_str = f"{file_size / (1024 * 1024):.2f} MB"

    # Prepare metadata summary
    metadata = data.get('metadata', {})
    metadata_summary = []
    for key, value in metadata.items():
        if value and value != 'Not Available' and value != 'No EXIF metadata found in image':
            metadata_summary.append(f"{key}: {value}")

    # Prepare notes
    notes = data.get('notes', 'Analysis completed successfully.')
    if not metadata_summary:
        notes += " No EXIF metadata was found in the image."

    if not data.get('ela_available', False):
        notes += " ELA analysis is only available for JPEG images."

    report = {
        'analysis_id': analysis_id,
        'timestamp': timestamp,
        'original_filename': data.get('filename', 'Unknown'),
        'file_size': file_size,
        'file_size_formatted': size_str,
        'format': data.get('format', 'Unknown'),
        'width': data.get('width', 0),
        'height': data.get('height', 0),
        'aspect_ratio': round(data.get('width', 0) / max(data.get('height', 1), 1), 2),
        'color_mode': data.get('mode', 'Unknown'),
        'metadata': metadata,
        'metadata_summary': metadata_summary,
        'hashes': data.get('hashes', {}),
        'ela_available': data.get('ela_available', False),
        'ela_result': data.get('ela_result'),
        'notes': notes
    }

    return report