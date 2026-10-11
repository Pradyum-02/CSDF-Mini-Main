from PIL import Image
import piexif
from datetime import datetime

def extract_metadata(image, filename):
    """Extract metadata from image"""
    metadata = {}

    # Basic image information
    metadata['Format'] = image.format if image.format else 'Unknown'
    metadata['Width'] = image.width
    metadata['Height'] = image.height
    metadata['Aspect Ratio'] = round(image.width / image.height, 2) if image.height > 0 else 0
    metadata['Color Mode'] = image.mode

    # EXIF data extraction
    try:
        exif_dict = {}
        if "exif" in image.info:
            exif_dict = piexif.load(image.info["exif"])

        # Camera information
        if exif_dict.get("0th"):
            if piexif.ImageIFD.Make in exif_dict["0th"]:
                make = exif_dict["0th"][piexif.ImageIFD.Make]
                metadata['Camera Make'] = make.decode('utf-8') if isinstance(make, bytes) else str(make)

            if piexif.ImageIFD.Model in exif_dict["0th"]:
                model = exif_dict["0th"][piexif.ImageIFD.Model]
                metadata['Camera Model'] = model.decode('utf-8') if isinstance(model, bytes) else str(model)

            if piexif.ImageIFD.Software in exif_dict["0th"]:
                software = exif_dict["0th"][piexif.ImageIFD.Software]
                metadata['Software'] = software.decode('utf-8') if isinstance(software, bytes) else str(software)

            if piexif.ImageIFD.DateTime in exif_dict["0th"]:
                datetime_str = exif_dict["0th"][piexif.ImageIFD.DateTime]
                dt = datetime_str.decode('utf-8') if isinstance(datetime_str, bytes) else str(datetime_str)
                metadata['DateTime Original'] = dt

        # GPS information
        if exif_dict.get("GPS"):
            gps_info = exif_dict["GPS"]
            if piexif.GPSIFD.GPSLatitude in gps_info and piexif.GPSIFD.GPSLongitude in gps_info:
                lat = _convert_gps_coordinate(gps_info[piexif.GPSIFD.GPSLatitude])
                lon = _convert_gps_coordinate(gps_info[piexif.GPSIFD.GPSLongitude])
                if lat is not None and lon is not None:
                    metadata['GPS Coordinates'] = f"{lat:.6f}, {lon:.6f}"

        # Exposure information
        if exif_dict.get("Exif"):
            exif_data = exif_dict["Exif"]

            if piexif.ExifIFD.ExposureTime in exif_data:
                exposure = exif_data[piexif.ExifIFD.ExposureTime]
                if isinstance(exposure, tuple) and len(exposure) == 2:
                    metadata['Exposure Time'] = f"{exposure[0]/exposure[1]} sec"
                else:
                    metadata['Exposure Time'] = str(exposure)

            if piexif.ExifIFD.FNumber in exif_data:
                aperture = exif_data[piexif.ExifIFD.FNumber]
                if isinstance(aperture, tuple) and len(aperture) == 2:
                    metadata['Aperture'] = f"f/{aperture[0]/aperture[1]:.1f}"
                else:
                    metadata['Aperture'] = str(aperture)

            if piexif.ExifIFD.ISOSpeedRatings in exif_data:
                iso = exif_data[piexif.ExifIFD.ISOSpeedRatings]
                metadata['ISO'] = str(iso)

            if piexif.ExifIFD.FocalLength in exif_data:
                focal = exif_data[piexif.ExifIFD.FocalLength]
                if isinstance(focal, tuple) and len(focal) == 2:
                    metadata['Focal Length'] = f"{focal[0]/focal[1]} mm"
                else:
                    metadata['Focal Length'] = str(focal)

    except Exception as e:
        # Handle cases where EXIF data is corrupted or unreadable
        metadata['EXIF Error'] = f"Unable to read EXIF data: {str(e)}"

    # If no meaningful metadata was found, indicate this
    meaningful_keys = [k for k, v in metadata.items() if v and v != 'Not Available' and k not in ['Format', 'Width', 'Height', 'Aspect Ratio', 'Color Mode']]
    if not meaningful_keys:
        metadata['Note'] = 'No EXIF metadata found in image'

    return metadata

def _convert_gps_coordinate(coord):
    """Convert GPS coordinates to decimal degrees"""
    try:
        if isinstance(coord, tuple) and len(coord) == 3:
            degrees, minutes, seconds = coord
            if isinstance(degrees, tuple) and len(degrees) == 2:
                degrees = degrees[0] / degrees[1]
            if isinstance(minutes, tuple) and len(minutes) == 2:
                minutes = minutes[0] / minutes[1]
            if isinstance(seconds, tuple) and len(seconds) == 2:
                seconds = seconds[0] / seconds[1]

            decimal = degrees + (minutes / 60) + (seconds / 3600)
            return decimal
    except Exception:
        pass
    return None