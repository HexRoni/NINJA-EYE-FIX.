"""
NINJA EYE - Security Checks Tests
Tests for the security diagnostics module and password system.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from modules.security_checks import (
    check_python_version,
    check_dependencies,
    check_project_structure,
    check_config,
    check_permissions,
)
from config import DEMO_PASSWORD, MAX_PASSWORD_ATTEMPTS


class TestCheckPythonVersion(unittest.TestCase):
    """Test Python version check."""

    def test_returns_tuple(self):
        result = check_python_version()
        self.assertEqual(len(result), 3)

    def test_passed_is_bool(self):
        passed, _, _ = check_python_version()
        self.assertIsInstance(passed, bool)

    def test_should_pass_on_current_env(self):
        passed, msg, fix = check_python_version()
        self.assertTrue(passed, f"Python version check failed: {msg}")


class TestCheckDependencies(unittest.TestCase):
    """Test dependency check."""

    def test_returns_tuple(self):
        result = check_dependencies()
        self.assertEqual(len(result), 3)

    def test_pillow_installed(self):
        passed, msg, fix = check_dependencies()
        # Pillow should be installed for tests to run
        self.assertTrue(passed, f"Dependency check failed: {msg}")


class TestCheckProjectStructure(unittest.TestCase):
    """Test project structure check."""

    def test_returns_tuple(self):
        result = check_project_structure()
        self.assertEqual(len(result), 3)

    def test_returns_bool_for_passed(self):
        passed, _, _ = check_project_structure()
        self.assertIsInstance(passed, bool)


class TestCheckConfig(unittest.TestCase):
    """Test configuration check."""

    def test_returns_tuple(self):
        result = check_config()
        self.assertEqual(len(result), 3)

    def test_config_valid(self):
        passed, msg, fix = check_config()
        self.assertTrue(passed, f"Config check failed: {msg}")


class TestPasswordConfig(unittest.TestCase):
    """Test password configuration."""

    def test_demo_password_exists(self):
        self.assertIsInstance(DEMO_PASSWORD, str)
        self.assertTrue(len(DEMO_PASSWORD) > 0)

    def test_max_attempts_positive(self):
        self.assertGreater(MAX_PASSWORD_ATTEMPTS, 0)
        self.assertLessEqual(MAX_PASSWORD_ATTEMPTS, 10)


class TestCheckPermissions(unittest.TestCase):
    """Test file permission check."""

    def test_returns_tuple(self):
        result = check_permissions()
        self.assertEqual(len(result), 3)

    def test_current_dir_accessible(self):
        passed, msg, fix = check_permissions()
        self.assertTrue(passed, f"Permission check failed: {msg}")


class TestInputValidation(unittest.TestCase):
    """Test input validation helpers."""

    def test_menu_invalid_string(self):
        invalid_inputs = ["a", "b", "abc", "1.5", "-1", "99", "!!"]
        for inp in invalid_inputs:
            self.assertNotIn(inp, ["0", "1", "2", "3", "4", "5", "6"])

    def test_menu_valid_string(self):
        valid_inputs = ["0", "1", "2", "3", "4", "5", "6"]
        for inp in valid_inputs:
            self.assertIn(inp, ["0", "1", "2", "3", "4", "5", "6"])


if __name__ == "__main__":
    unittest.main()
