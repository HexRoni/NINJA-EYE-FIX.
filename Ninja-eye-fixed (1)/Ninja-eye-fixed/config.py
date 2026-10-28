"""
NINJA EYE - Configuration File
Store all project settings here.
"""

# ─── Project Info ────────────────────────────────────────────────
PROJECT_NAME = "NINJA EYE"
VERSION = "1.0.0"
AUTHOR = "NINJA EYE Team"

# ─── Password Settings ───────────────────────────────────────────
# WARNING: This is a DEMO password embedded in source code.
# It is NOT secure. For production, use environment variables
# or an encrypted config file outside the repository.
DEMO_PASSWORD = "NINJA"
MAX_PASSWORD_ATTEMPTS = 3

# ─── Image Analyzer Settings ────────────────────────────────────
MAX_IMAGE_SIZE_MB = 50  # Reject images larger than this
MAX_IMAGE_SIZE_BYTES = MAX_IMAGE_SIZE_MB * 1024 * 1024

# ─── Lab Mode Settings ──────────────────────────────────────────
LAB_HOST = "127.0.0.1"  # Always localhost
LAB_PORT_RANGE = (1024, 65535)

# ─── Menu Settings ──────────────────────────────────────────────
MENU_WIDTH = 50

# ─── Paths ──────────────────────────────────────────────────────
PROJECT_ROOT = "."  # Set by main program
