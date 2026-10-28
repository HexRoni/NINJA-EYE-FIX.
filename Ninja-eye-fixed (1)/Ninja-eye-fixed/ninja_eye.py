#!/usr/bin/env python3
"""
NINJA EYE - Python Security Learning Tool
A beginner-friendly educational security tool for Kali Linux.

This tool is for AUTHORIZED educational and defensive security learning only.
"""

import sys
import os
import getpass

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import PROJECT_NAME, VERSION, DEMO_PASSWORD, MAX_PASSWORD_ATTEMPTS, MENU_WIDTH
from modules.network_analyzer import display_info
from modules.image_analyzer import analyze_image
from modules.lab_mode import lab_menu
from modules.security_checks import run_all_checks


def clear_screen():
    """Clear the terminal screen."""
    os.system("clear" if os.name != "nt" else "cls")


def show_banner():
    """Display the NINJA EYE banner."""
    print("=" * MENU_WIDTH)
    print(f"  {PROJECT_NAME}")
    print(f"  Python Security Learning Tool v{VERSION}")
    print("=" * MENU_WIDTH)


def password_prompt() -> bool:
    """
    Request password before showing main menu.
    Returns True if authenticated, False if max attempts exceeded.

    WARNING: This is a DEMO password protection system.
    Passwords in source code are NOT secure.
    """
    print(f"\n  🔒 {PROJECT_NAME} requires a password to continue.")
    print(f"  (Demo password: NINJA)\n")

    for attempt in range(1, MAX_PASSWORD_ATTEMPTS + 1):
        try:
            password = getpass.getpass(f"  Password (attempt {attempt}/{MAX_PASSWORD_ATTEMPTS}): ")
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Cancelled by user.")
            return False

        if password == DEMO_PASSWORD:
            print(f"\n  ✅ Access granted. Welcome!\n")
            return True
        else:
            remaining = MAX_PASSWORD_ATTEMPTS - attempt
            if remaining > 0:
                print(f"  ❌ Wrong password. {remaining} attempt(s) remaining.\n")
            else:
                print(f"\n  ❌ Too many failed attempts. Exiting.")
                print(f"\n  ⚠️  Note: Password protection in source code is NOT secure.")
                print(f"     This is a demo feature only.")

    return False


def show_main_menu():
    """Display the main menu options."""
    print(f"""
  [1] Local IP Information
  [2] Image Metadata Analyzer
  [3] Laboratory Mode
  [4] Run Security Checks
  [5] Help and Documentation
  [6] Run Self-Test
  [0] Exit
""")


def show_help():
    """Display help and documentation."""
    print("\n" + "=" * MENU_WIDTH)
    print("  HELP & DOCUMENTATION")
    print("=" * MENU_WIDTH)
    print(f"""
  ABOUT:
    {PROJECT_NAME} v{VERSION} is a beginner-friendly security
    learning tool. It helps you understand network basics,
    image metadata, and security concepts in a safe way.

  FEATURES:
    [1] Local IP Information
        → Shows your machine's hostname and local IP address.
        → Explains the difference between private and public IPs.

    [2] Image Metadata Analyzer
        → Reads EXIF metadata embedded in image files.
        → Warns about GPS location data in photos.
        → Helps you understand what information you share.

    [3] Laboratory Mode
        → Safe experiments on localhost (127.0.0.1) only.
        → Port checker, hash calculator, permission checker.
        → No external scanning or tracking.

    [4] Run Security Checks
        → Verifies your Python environment is correct.
        → Checks all required files are present.
        → Shows fix suggestions if something is wrong.

    [6] Run Self-Test
        → Quick verification that everything is ready.
        → Shows a simple status report.

  SECURITY NOTICE:
    This tool is for EDUCATIONAL purposes only.
    Do not use it for unauthorized activities.
    Always respect privacy and local laws.

  MORE HELP:
    docs/installation.md   → Setup guide
    docs/usage.md          → How to use each feature
    docs/troubleshooting.md → Fix common problems
""")
    print("=" * MENU_WIDTH)


def run_self_test():
    """Run the built-in self-test."""
    print("\n" + "=" * MENU_WIDTH)
    print("  NINJA EYE SELF-TEST")
    print("=" * MENU_WIDTH)

    from modules.security_checks import (
        check_python_version,
        check_dependencies,
        check_project_structure,
        check_config,
    )

    results = []

    # Python version
    passed, msg, fix = check_python_version()
    results.append(("Python Environment", passed, msg, fix))

    # Dependencies
    passed, msg, fix = check_dependencies()
    results.append(("Dependencies", passed, msg, fix))

    # Project structure
    passed, msg, fix = check_project_structure()
    results.append(("Project Structure", passed, msg, fix))

    # Configuration
    passed, msg, fix = check_config()
    results.append(("Configuration", passed, msg, fix))

    # Display
    print()
    for name, ok, msg, fix in results:
        icon = "✅" if ok else "❌"
        print(f"  {name:20s}: {icon} {msg}")
        if not ok and fix:
            print(f"  {'':20s}  └─ Fix: {fix}")

    all_ok = all(ok for _, ok, _, _ in results)
    print("\n" + "-" * MENU_WIDTH)
    if all_ok:
        print(f"  Overall Status: ✅ READY")
    else:
        print(f"  Overall Status: ❌ NOT READY")
        print(f"  Fix the issues above and try again.")
    print("=" * MENU_WIDTH)


def image_analyzer_menu():
    """Handle the image analyzer sub-menu."""
    print("\n  ── Image Metadata Analyzer ──")
    print("  Enter the path of an image file to analyze its metadata.")
    print("  Example: /home/user/photos/vacation.jpg")
    print("  Tip: You can drag-and-drop a file into the terminal.\n")

    path = input("  Image path (or 'q' to go back): ").strip()

    if path.lower() in ('q', 'quit', 'back', ''):
        return

    analyze_image(path)


def main():
    """Main program entry point."""
    clear_screen()
    show_banner()

    # Password protection
    if not password_prompt():
        sys.exit(1)

    clear_screen()
    show_banner()

    # Main loop
    while True:
        show_main_menu()
        try:
            choice = input("  Select an option: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\n  👋 Goodbye! Stay safe!")
            sys.exit(0)

        if choice == "1":
            try:
                display_info()
            except Exception as e:
                print(f"\n  ❌ Unexpected error: {e}")
                print(f"  Run Security Checks [option 4] to diagnose.")
        elif choice == "2":
            try:
                image_analyzer_menu()
            except Exception as e:
                print(f"\n  ❌ Unexpected error: {e}")
        elif choice == "3":
            try:
                lab_menu()
            except Exception as e:
                print(f"\n  ❌ Unexpected error: {e}")
        elif choice == "4":
            try:
                run_all_checks()
            except Exception as e:
                print(f"\n  ❌ Unexpected error: {e}")
        elif choice == "5":
            show_help()
        elif choice == "6":
            run_self_test()
        elif choice == "0":
            print(f"\n  👋 Goodbye! Stay safe out there!\n")
            sys.exit(0)
        else:
            print(f"\n  ❌ Invalid option: '{choice}'")
            print(f"  Please enter a number from 0-6.\n")
            continue

        if choice not in ("0",):
            input(f"\n  Press Enter to return to main menu...")
            clear_screen()
            show_banner()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  👋 Interrupted. Goodbye!\n")
        sys.exit(0)
