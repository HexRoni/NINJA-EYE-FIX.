"""
NINJA EYE - Image Metadata Analyzer Module
Reads and displays EXIF metadata from image files.
"""

import os
import sys
from typing import Optional
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from config import MAX_IMAGE_SIZE_BYTES, MAX_IMAGE_SIZE_MB

MODULE_NAME = "Image Metadata Analyzer"


def validate_path(path: str) -> tuple:
    """
    Validate that the image path exists and is readable.
    Returns (is_valid, error_message).
    """
    if not path or not path.strip():
        return False, "Please enter a file path."

    path = path.strip().strip("'\"")

    if not os.path.exists(path):
        return False, f"File not found: {path}\n  Check the path and try again."

    if not os.path.isfile(path):
        return False, f"'{path}' is a directory, not a file."

    if not os.access(path, os.R_OK):
        return False, f"Permission denied: Cannot read '{path}'\n  Try: chmod +r '{path}'"

    # Check file size
    file_size = os.path.getsize(path)
    if file_size > MAX_IMAGE_SIZE_BYTES:
        size_mb = file_size / (1024 * 1024)
        return False, (
            f"File too large: {size_mb:.1f} MB\n"
            f"  Maximum allowed: {MAX_IMAGE_SIZE_MB} MB\n"
            f"  Use a smaller image file."
        )

    if file_size == 0:
        return False, "File is empty (0 bytes)."

    return True, ""


def extract_exif(image: Image.Image) -> dict:
    """Extract EXIF data from a PIL Image object."""
    exif_data = {}
    try:
        exif = image.getexif()
        if not exif:
            return exif_data
        for tag_id, value in exif.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo" and hasattr(exif, "get_ifd"):
                try:
                    value = exif.get_ifd(tag_id)
                except (KeyError, TypeError, ValueError):
                    pass
            exif_data[tag] = value
    except (AttributeError, OSError, ValueError, TypeError):
        # Some formats and malformed files do not expose readable EXIF.
        pass
    return exif_data


def extract_gps(exif_data: dict) -> Optional[dict]:
    """Extract GPS information from EXIF data if present."""
    gps_info = exif_data.get("GPSInfo")
    if not gps_info:
        return None
    gps = {}
    for key, val in gps_info.items():
        tag = GPSTAGS.get(key, key)
        gps[tag] = val
    return gps


def format_value(value) -> str:
    """Format EXIF values for display."""
    if isinstance(value, bytes):
        try:
            return value.decode("utf-8", errors="replace")
        except Exception:
            return repr(value)
    elif isinstance(value, tuple):
        return " / ".join(str(v) for v in value)
    return str(value)


def analyze_image(path: str) -> None:
    """Main function: analyze an image and display metadata."""
    # Validate
    valid, error = validate_path(path)
    if not valid:
        print(f"\n  ❌ Error: {error}")
        return

    path = path.strip().strip("'\"")
    file_size = os.path.getsize(path)

    print("\n" + "=" * 50)
    print("  IMAGE METADATA ANALYZER")
    print("=" * 50)
    print(f"\n  File: {os.path.basename(path)}")
    print(f"  Size: {file_size / 1024:.1f} KB")

    # Try to open the image
    try:
        image = Image.open(path)
    except Exception:
        print(f"\n  ❌ Error: Cannot open as image.")
        print(f"     The file may be corrupted or not a valid image format.")
        print(f"     Supported: JPG, PNG, GIF, BMP, TIFF, WebP")
        return

    # Basic info
    print(f"\n  ── Basic Information ──")
    print(f"  Format    : {image.format}")
    print(f"  Dimensions: {image.width} x {image.height} pixels")
    print(f"  Mode      : {image.mode}")

    # EXIF data
    exif_data = extract_exif(image)

    if not exif_data:
        print(f"\n  ── EXIF Metadata ──")
        print(f"  No EXIF metadata found.")
        print(f"  This is common for PNG files or images stripped of metadata.")
        print(f"\n  💡 Tip: Photos taken with smartphones/cameras usually have EXIF data.")
    else:
        print(f"\n  ── EXIF Metadata ({len(exif_data)} tags) ──")
        for tag, value in sorted(exif_data.items()):
            if tag == "GPSInfo":
                continue  # Handle separately
            formatted = format_value(value)
            if len(formatted) > 60:
                formatted = formatted[:57] + "..."
            print(f"  {tag:30s}: {formatted}")

    # GPS check
    gps = extract_gps(exif_data)
    if gps:
        print(f"\n  ⚠️  GPS LOCATION DATA FOUND!")
        print(f"  ─────────────────────────────")
        for tag, value in sorted(gps.items()):
            print(f"  {tag:30s}: {value}")
        print(f"\n  🚨 WARNING: This image contains GPS coordinates!")
        print(f"  Anyone with this image can determine WHERE it was taken.")
        print(f"  Before sharing, remove GPS data using:")
        print(f"    exiftool -gps:all= <filename>")
    else:
        print(f"\n  GPS Data: Not found ✓ (safe)")

    # Sensitive metadata warnings
    sensitive_tags = ["Software", "Artist", "Copyright", "Make", "Model",
                      "DateTimeOriginal", "LensModel", "SerialNumber"]
    found_sensitive = [t for t in sensitive_tags if t in exif_data]

    if found_sensitive:
        print(f"\n  ⚠️  Potentially Sensitive Metadata Found:")
        for tag in found_sensitive:
            print(f"     • {tag}: {format_value(exif_data[tag])}")
        print(f"\n  💡 To remove all metadata before sharing:")
        print(f"     exiftool -all= <filename>")

    print("\n" + "=" * 50)
