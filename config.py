"""
Configuration settings for the voting application.

This module contains all the configuration variables used across the application.
"""
from typing import Dict, List
from pathlib import Path

# File paths
DATA_DIR: Path = Path("data")
VOTES_FILE: Path = DATA_DIR / "votes.csv"
VOTERS_FILE: Path = DATA_DIR / "voters.csv"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(exist_ok=True)

# Candidates list
CANDIDATES: list[str] = [
    "Leonardo DiCaprio",
    "Marlon Brando",
    "Johnny Depp",
    "Christian Bale"
]

# GUI Configuration
WINDOW_TITLE: str = "Best Actor Application"
WINDOW_SIZE: tuple[int, int] = (450, 600)

# Modern color scheme (Used  color codes & font info from tutorials & site)
COLORS = {
    "primary": "#2563eb",  # Blue
    "background": "#f8fafc", # Light gray
    "text": "#1e293b",  # Dark blue-gray
    "error": "#ef4444",  # Red
    "success": "#22c55e",  # Green
    "button": "#3b82f6",  # Light blue
    "button_hover": "#1d4ed8",  # Darker blue
}

# Font settings
FONTS = {
    "title": ("Helvetica", 24, "bold"),
    "header": ("Helvetica", 18),
    "normal": ("Helvetica", 12),
    "button": ("Helvetica", 12, "bold")
}

# ID Validation
ID_MIN_LENGTH: int = 4
ID_MAX_LENGTH: int = 10
ID_PATTERN: str = r'^[A-Za-z0-9]+$'  # Alphanumeric only