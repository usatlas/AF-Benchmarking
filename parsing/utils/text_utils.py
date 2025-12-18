"""Text processing utilities for log parsing.

This module provides common text manipulation functions used across
different log parsers.
"""

import re


# Regex pattern to match ANSI escape sequences (color codes, etc.)
ANSI_ESCAPE = re.compile(r"\x1B\[[0-?]*[ -/]*[@-~]")


def strip_ansi(text):
    """Remove ANSI escape sequences from text.

    ANSI escape sequences are used for terminal colors and formatting.
    This function removes them to get clean text for parsing.

    Args:
        text (str): Text potentially containing ANSI codes

    Returns:
        str: Text with ANSI codes removed

    Example:
        >>> strip_ansi("\\x1B[32mGreen text\\x1B[0m")
        'Green text'
    """
    return ANSI_ESCAPE.sub("", text)
