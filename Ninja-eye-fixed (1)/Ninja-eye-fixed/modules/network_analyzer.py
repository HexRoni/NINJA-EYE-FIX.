"""
NINJA EYE - Local IP Information Module
Displays network information about the user's own machine.
"""

import socket
import subprocess
import sys
from typing import Optional

MODULE_NAME = "Network Analyzer"


def get_hostname() -> str:
    """Return the system hostname."""
    try:
        return socket.gethostname()
    except OSError:
        return "Unknown"


def get_local_ip() -> Optional[str]:
    """
    Get the local IPv4 address by opening a UDP socket.
    Does not send any data — just determines the routing interface.
    Returns None if network is unavailable.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(3)
        # UDP connect selects a route; no application data is sent.
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except (OSError, socket.timeout):
        return None
    finally:
        try:
            s.close()
        except (UnboundLocalError, OSError):
            pass


def get_interfaces() -> list:
    """
    Get network interface information using `ip addr` command.
    Returns a list of (interface_name, ip_address) tuples.
    """
    interfaces = []
    try:
        result = subprocess.run(
            ["ip", "-4", "addr", "show"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            lines = result.stdout.split("\n")
            current_iface = ""
            for line in lines:
                line = line.strip()
                # Interface header lines start with an index followed by a colon.
                if line and line[0].isdigit() and ": " in line:
                    parts = line.split(": ", 1)
                    if len(parts) == 2:
                        current_iface = parts[1].split("@")[0]
                if "inet " in line and current_iface:
                    ip = line.split("inet ")[1].split("/")[0].strip()
                    interfaces.append((current_iface, ip))
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return interfaces


def display_info() -> None:
    """Display all local network information to the user."""
    print("\n" + "=" * 50)
    print("  LOCAL IP INFORMATION")
    print("=" * 50)

    # Hostname
    hostname = get_hostname()
    print(f"\n  Hostname: {hostname}")

    # Local IP
    print("\n  Checking network connection...")
    local_ip = get_local_ip()

    if local_ip is None:
        print("\n  ⚠️  Network appears to be DISCONNECTED.")
        print("     No active network interface with an IPv4 address found.")
        print("\n  Possible fixes:")
        print("     1. Check if WiFi or Ethernet cable is connected.")
        print("     2. Run: sudo systemctl restart NetworkManager")
        print("     3. Check: ip addr  (to see available interfaces)")
    else:
        print(f"\n  Local IPv4 Address : {local_ip}")
        print(f"  Status             : Connected ✓")

        # Private vs Public explanation
        print("\n  ── IP Address Explanation ──")
        print(f"  Your Private IP: {local_ip}")
        print("  → This is your address inside your local network (WiFi/LAN).")
        print("  → Only devices on the SAME network can see this.")
        print("\n  Your Public IP:")
        print("  → This is assigned by your ISP (Internet Provider).")
        print("  → Websites see this address when you visit them.")
        print("  → NINJA EYE does NOT fetch or display public IPs.")

    # Interfaces
    print("\n  ── Network Interfaces ──")
    interfaces = get_interfaces()
    if interfaces:
        for iface, ip in interfaces:
            print(f"  • {iface:15s} → {ip}")
    else:
        print("  No interface information available.")
        print("  Try running: ip addr")

    print("\n" + "=" * 50)
