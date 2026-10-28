"""
NINJA EYE - Security Checks Module
Runs diagnostic checks on the project environment.
"""

import os
import sys
import importlib
from typing import Optional

MODULE_NAME = "Security Checks"
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Expected project files
REQUIRED_FILES = [
    "ninja_eye.py",
    "config.py",
    "requirements.txt",
    "modules/__init__.py",
    "modules/network_analyzer.py",
    "modules/image_analyzer.py",
    "modules/lab_mode.py",
    "modules/security_checks.py",
]

REQUIRED_MODULES = ["PIL"]

REQUIRED_PYTHON_VERSION = (3, 8)


def check_python_version() -> tuple:
    """Check Python version. Returns (passed, message, fix_hint)."""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    if version.major >= 3 and version.minor >= REQUIRED_PYTHON_VERSION[1]:
        return True, f"Python {version_str}", ""
    return False, f"Python {version_str} (requires 3.8+)", "Install Python 3.8 or newer"


def check_dependencies() -> tuple:
    """Check required Python packages. Returns (passed, message, fix_hint)."""
    missing = []
    for module_name in REQUIRED_MODULES:
        try:
            importlib.import_module(module_name)
        except ImportError:
            missing.append(module_name)

    if missing:
        modules_str = ", ".join(missing)
        return False, f"Missing: {modules_str}", f"Run: pip install {' '.join(missing)}"
    return True, f"All {len(REQUIRED_MODULES)} dependencies installed", ""


def check_project_structure() -> tuple:
    """Check required project files exist. Returns (passed, message, fix_hint)."""
    missing_files = []
    for filepath in REQUIRED_FILES:
        if not os.path.exists(os.path.join(PROJECT_ROOT, filepath)):
            missing_files.append(filepath)

    if missing_files:
        files_str = ", ".join(missing_files[:3])
        if len(missing_files) > 3:
            files_str += f" (+{len(missing_files) - 3} more)"
        return False, f"Missing files: {files_str}", "Re-download the project from GitHub"
    return True, f"All {len(REQUIRED_FILES)} project files present", ""


def check_config() -> tuple:
    """Check config file is valid. Returns (passed, message, fix_hint)."""
    try:
        if PROJECT_ROOT not in sys.path:
            sys.path.insert(0, PROJECT_ROOT)
        import config
        required_vars = ["PROJECT_NAME", "VERSION", "DEMO_PASSWORD",
                         "MAX_PASSWORD_ATTEMPTS", "MAX_IMAGE_SIZE_BYTES"]
        missing_vars = []
        for var in required_vars:
            if not hasattr(config, var):
                missing_vars.append(var)

        if missing_vars:
            vars_str = ", ".join(missing_vars)
            return False, f"Missing config variables: {vars_str}", "Restore config.py from GitHub"
        return True, "Configuration valid", ""
    except ImportError:
        return False, "Cannot import config.py", "Ensure config.py is in the project root"
    except Exception as e:
        return False, f"Config error: {e}", "Check config.py for syntax errors"


def check_permissions() -> tuple:
    """Check file permissions on project files. Returns (passed, message, fix_hint)."""
    current_dir = PROJECT_ROOT
    if not os.access(current_dir, os.R_OK | os.W_OK):
        return False, "No read/write permission on project directory", f"chmod -R u+rw {current_dir}"

    # Check specific files
    for filepath in REQUIRED_FILES:
        full_path = os.path.join(PROJECT_ROOT, filepath)
        if os.path.exists(full_path) and not os.access(full_path, os.R_OK):
            return False, f"Cannot read: {filepath}", f"chmod +r '{full_path}'"

    return True, "File permissions OK", ""


def run_all_checks() -> bool:
    """Run all security checks. Returns True if all passed."""
    print("\n" + "=" * 50)
    print("  SECURITY CHECKS")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Configuration", check_config),
        ("File Permissions", check_permissions),
    ]

    all_passed = True
    results = []

    print()
    for name, check_func in checks:
        passed, message, fix = check_func()
        status = "✓ OK" if passed else "✗ FAIL"
        results.append((name, passed, message, fix))

        if not passed:
            all_passed = False

    # Display results
    for name, passed, message, fix in results:
        status_icon = "✅" if passed else "❌"
        print(f"  {status_icon} {name:20s} : {message}")
        if not passed and fix:
            print(f"     └─ Fix: {fix}")

    print("\n" + "-" * 50)
    if all_passed:
        print(f"  Result: ✅ ALL CHECKS PASSED")
    else:
        failed_count = sum(1 for _, p, _, _ in results if not p)
        print(f"  Result: ❌ {failed_count} check(s) FAILED")
        print(f"  Follow the fix suggestions above.")
    print("=" * 50)

    return all_passed
