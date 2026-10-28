"""
NINJA EYE - Image Analyzer Tests
Tests for the image metadata analyzer module.
"""

import unittest
import os
import sys
import tempfile
import struct

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.image_analyzer import (
    validate_path,
    extract_exif,
    extract_gps,
    format_value,
)

from PIL import Image

try:
    from PIL import PngImagePlugin
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


class TestValidatePath(unittest.TestCase):
    """Test path validation."""

    def test_empty_path(self):
        valid, msg = validate_path("")
        self.assertFalse(valid)
        self.assertIn("path", msg.lower())

    def test_whitespace_path(self):
        valid, msg = validate_path("   ")
        self.assertFalse(valid)

    def test_nonexistent_file(self):
        valid, msg = validate_path("/nonexistent/file.jpg")
        self.assertFalse(valid)
        self.assertIn("not found", msg.lower())

    def test_directory_instead_of_file(self):
        valid, msg = validate_path("/tmp")
        self.assertFalse(valid)
        self.assertIn("directory", msg.lower())

    def test_valid_image(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            img = Image.new("RGB", (10, 10), color="red")
            img.save(f.name, "JPEG")
            path = f.name
        try:
            valid, msg = validate_path(path)
            self.assertTrue(valid)
        finally:
            os.unlink(path)

    def test_empty_file(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
            path = f.name
        try:
            valid, msg = validate_path(path)
            self.assertFalse(valid)
            self.assertIn("empty", msg.lower())
        finally:
            os.unlink(path)

    def test_file_too_large(self):
        import modules.image_analyzer as ia
        original_limit = ia.MAX_IMAGE_SIZE_BYTES
        try:
            ia.MAX_IMAGE_SIZE_BYTES = 1  # 1 byte limit
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as f:
                f.write(b"\x00" * 100)
                path = f.name
            try:
                valid, msg = validate_path(path)
                self.assertFalse(valid)
                self.assertIn("too large", msg.lower())
            finally:
                os.unlink(path)
        finally:
            ia.MAX_IMAGE_SIZE_BYTES = original_limit


class TestExtractExif(unittest.TestCase):
    """Test EXIF extraction."""

    def test_image_without_exif(self):
        img = Image.new("RGB", (10, 10), color="blue")
        result = extract_exif(img)
        # PNG images typically have no EXIF
        self.assertIsInstance(result, dict)

    def test_image_with_exif(self):
        img = Image.new("RGB", (10, 10), color="green")
        # Create EXIF data
        exif_dict = {
            271: "TestMake",      # Make
            272: "TestModel",     # Model
            306: "2024:01:01 00:00:00"  # DateTime
        }
        from PIL.ExifTags import TAGS
        exif_bytes = Image.Exif()
        for tag_id, value in exif_dict.items():
            exif_bytes[tag_id] = value
        img.save("/tmp/test_exif_img.jpg", "JPEG", exif=exif_bytes)
        try:
            with Image.open("/tmp/test_exif_img.jpg") as reopened:
                result = extract_exif(reopened)
            self.assertIsInstance(result, dict)
            self.assertTrue(len(result) > 0)
        finally:
            os.unlink("/tmp/test_exif_img.jpg")


class TestExtractGPS(unittest.TestCase):
    """Test GPS extraction."""

    def test_no_gps(self):
        exif_data = {"Make": "TestCamera"}
        result = extract_gps(exif_data)
        self.assertIsNone(result)

    def test_empty_exif(self):
        result = extract_gps({})
        self.assertIsNone(result)


class TestFormatValue(unittest.TestCase):
    """Test value formatting."""

    def test_bytes_value(self):
        result = format_value(b"TestValue")
        self.assertEqual(result, "TestValue")

    def test_tuple_value(self):
        result = format_value((1, 2, 3))
        self.assertEqual(result, "1 / 2 / 3")

    def test_string_value(self):
        result = format_value("hello")
        self.assertEqual(result, "hello")

    def test_int_value(self):
        result = format_value(42)
        self.assertEqual(result, "42")


if __name__ == "__main__":
    unittest.main()
