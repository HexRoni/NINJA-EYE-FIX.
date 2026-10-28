"""
NINJA EYE - Network Analyzer Tests
Tests for the local IP information module.
"""

import unittest
from unittest.mock import patch, MagicMock
import socket
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.network_analyzer import (
    get_hostname,
    get_local_ip,
    get_interfaces,
)


class TestGetHostname(unittest.TestCase):
    """Test hostname retrieval."""

    def test_returns_string(self):
        result = get_hostname()
        self.assertIsInstance(result, str)

    def test_returns_non_empty(self):
        result = get_hostname()
        self.assertTrue(len(result) > 0)

    @patch("socket.gethostname", side_effect=OSError("Network error"))
    def test_handles_oserror(self, mock_hostname):
        result = get_hostname()
        self.assertEqual(result, "Unknown")


class TestGetLocalIP(unittest.TestCase):
    """Test local IP address detection."""

    def test_returns_string_or_none(self):
        result = get_local_ip()
        self.assertTrue(result is None or isinstance(result, str))

    def test_valid_ip_format_if_connected(self):
        result = get_local_ip()
        if result is not None:
            parts = result.split(".")
            self.assertEqual(len(parts), 4)
            for part in parts:
                self.assertTrue(0 <= int(part) <= 255)

    @patch("socket.socket")
    def test_returns_none_on_connection_failure(self, mock_socket):
        mock_socket.side_effect = OSError("Network unreachable")
        result = get_local_ip()
        self.assertIsNone(result)


class TestGetInterfaces(unittest.TestCase):
    """Test network interface enumeration."""

    def test_returns_list(self):
        result = get_interfaces()
        self.assertIsInstance(result, list)

    def test_tuples_have_two_elements(self):
        result = get_interfaces()
        for item in result:
            self.assertEqual(len(item), 2)
            self.assertIsInstance(item[0], str)
            self.assertIsInstance(item[1], str)


if __name__ == "__main__":
    unittest.main()
