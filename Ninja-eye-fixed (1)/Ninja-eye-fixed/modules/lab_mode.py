"""
NINJA EYE - Laboratory Mode
Safe, localhost-only experiments for learning security concepts.
All experiments operate on the user's own machine only.
"""

import socket
import hashlib
import os
import stat
from config import LAB_HOST

MODULE_NAME = "Laboratory Mode"


def lab_menu() -> None:
    """Display lab mode submenu."""
    while True:
        print("\n" + "=" * 50)
        print("  LABORATORY MODE")
        print("  Safe experiments on localhost only")
        print("=" * 50)
        print("""
  [1] Local Port Checker
  [2] File Hash Calculator
  [3] File Permission Checker
  [4] Back to Main Menu
""")
        choice = input("  Select an experiment: ").strip()

        if choice == "1":
            local_port_checker()
        elif choice == "2":
            file_hash_calculator()
        elif choice == "3":
            file_permission_checker()
        elif choice == "4" or choice == "0":
            break
        else:
            print("\n  ❌ Invalid choice. Please enter 1-4.")

        if choice not in ("4", "0"):
            input("\n  Press Enter to return to Lab Menu...")


def local_port_checker() -> None:
    """Check which local ports are open on localhost."""
    print("\n  ── Local Port Checker ──")
    print("  This checks which ports are OPEN on your own machine (127.0.0.1).")
    print("  It does NOT scan any other computer.\n")

    try:
        start = int(input("  Start port (default 1024): ").strip() or "1024")
        end = int(input("  End port   (default 1100): ").strip() or "1100")
    except ValueError:
        print("  ❌ Invalid port number. Please enter numbers only.")
        return

    if start < 1 or end > 65535 or start > end:
        print("  ❌ Invalid port range. Ports must be 1-65535.")
        return

    if (end - start) > 500:
        print("  ❌ Range too large. Maximum 500 ports at a time.")
        return

    print(f"\n  Scanning ports {start}-{end} on {LAB_HOST}...\n")
    open_ports = []

    for port in range(start, end + 1):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            result = sock.connect_ex((LAB_HOST, port))
            sock.close()
            if result == 0:
                open_ports.append(port)
        except (OSError, socket.timeout):
            pass

    if open_ports:
        print(f"  Open ports found ({len(open_ports)}):")
        for port in open_ports:
            service = get_common_service(port)
            print(f"  • Port {port:5d} — {service}")
    else:
        print("  No open ports found in the specified range.")
        print("  💡 Tip: Start a local server first (e.g., python3 -m http.server 8080)")

    print(f"\n  Scan complete. Scanned {end - start + 1} ports.")


def get_common_service(port: int) -> str:
    """Return common service name for well-known ports."""
    services = {
        22: "SSH", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
        5432: "PostgreSQL", 8080: "HTTP Alt", 21: "FTP",
        25: "SMTP", 53: "DNS", 3389: "RDP", 139: "NetBIOS",
        445: "SMB", 6379: "Redis", 27017: "MongoDB"
    }
    return services.get(port, "Unknown Service")


def file_hash_calculator() -> None:
    """Calculate MD5, SHA1, SHA256 hash of a local file."""
    print("\n  ── File Hash Calculator ──")
    print("  Calculates cryptographic hashes of any local file.")
    print("  Hashes are used to verify file integrity.\n")

    path = input("  Enter file path: ").strip().strip("'\"")

    if not path:
        print("  ❌ Please enter a path.")
        return

    if not os.path.exists(path):
        print(f"  ❌ File not found: {path}")
        return

    if not os.path.isfile(path):
        print(f"  ❌ Not a file: {path}")
        return

    file_size = os.path.getsize(path)
    if file_size > 100 * 1024 * 1024:  # 100MB limit
        print("  ❌ File too large for hash calculation (max 100 MB).")
        return

    try:
        md5 = hashlib.md5()
        sha1 = hashlib.sha1()
        sha256 = hashlib.sha256()

        with open(path, "rb") as f:
            while True:
                chunk = f.read(8192)
                if not chunk:
                    break
                md5.update(chunk)
                sha1.update(chunk)
                sha256.update(chunk)

        print(f"\n  File: {os.path.basename(path)}")
        print(f"  Size: {file_size / 1024:.1f} KB")
        print(f"\n  MD5    : {md5.hexdigest()}")
        print(f"  SHA1   : {sha1.hexdigest()}")
        print(f"  SHA256 : {sha256.hexdigest()}")
    except (PermissionError, OSError) as e:
        print(f"  ❌ Cannot read file: {e}")


def file_permission_checker() -> None:
    """Check and explain file permissions of a given path."""
    print("\n  ── File Permission Checker ──")
    print("  Shows Unix file permissions in human-readable format.\n")

    path = input("  Enter file or directory path: ").strip().strip("'\"")

    if not path:
        print("  ❌ Please enter a path.")
        return

    if not os.path.exists(path):
        print(f"  ❌ Path not found: {path}")
        return

    try:
        st = os.stat(path)
        mode = st.st_mode

        # Permission string
        perms = stat.filemode(mode)

        # Detailed breakdown
        owner_read = bool(mode & stat.S_IRUSR)
        owner_write = bool(mode & stat.S_IWUSR)
        owner_exec = bool(mode & stat.S_IXUSR)
        group_read = bool(mode & stat.S_IRGRP)
        group_write = bool(mode & stat.S_IWGRP)
        group_exec = bool(mode & stat.S_IXGRP)
        other_read = bool(mode & stat.S_IROTH)
        other_write = bool(mode & stat.S_IWOTH)
        other_exec = bool(mode & stat.S_IXOTH)

        print(f"\n  Path: {path}")
        print(f"  Permissions: {perms}")
        print(f"  Size: {st.st_size} bytes")

        if os.path.isdir(path):
            print(f"  Type: Directory")
        else:
            print(f"  Type: File")

        print(f"\n  ── Breakdown ──")
        print(f"  Owner: Read={'Yes' if owner_read else 'No'} "
              f"Write={'Yes' if owner_write else 'No'} "
              f"Execute={'Yes' if owner_exec else 'No'}")
        print(f"  Group: Read={'Yes' if group_read else 'No'} "
              f"Write={'Yes' if group_write else 'No'} "
              f"Execute={'Yes' if group_exec else 'No'}")
        print(f"  Other: Read={'Yes' if other_read else 'No'} "
              f"Write={'Yes' if other_write else 'No'} "
              f"Execute={'Yes' if other_exec else 'No'}")

        # Security warnings
        if other_write and not os.path.isdir(path):
            print(f"\n  ⚠️  WARNING: World-writable file detected!")
            print(f"     Anyone can modify this file.")
            print(f"     Fix: chmod o-w '{path}'")

        if owner_exec and not os.path.isdir(path) and not path.endswith(('.py', '.sh')):
            print(f"\n  ⚠️  File is executable but not a script.")
            print(f"     Verify this is intentional.")

        if not other_read and not group_read and not owner_read:
            print(f"\n  ⚠️  File has NO read permission for anyone.")

    except (PermissionError, OSError) as e:
        print(f"  ❌ Cannot access: {e}")
