# log_util.py
# A homemade logger. Modernised style in 2026.

import time

LOG_LINES: list = []    # global state, shared by everyone who imports this
DEBUG = False


def log(message: str) -> None:
    """Timestamp message, print it, and buffer it for the next flush_log call."""
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {message}"
    LOG_LINES.append(line)
    print(line)


def debug(message: str) -> None:
    """Log a DEBUG-prefixed message — only active when DEBUG is True."""
    if DEBUG:
        log(f"DEBUG: {message}")


def flush_log(path: str) -> None:
    """Append all buffered log lines to path and clear the buffer."""
    with open(path, "a") as f:
        for line in LOG_LINES:
            f.write(line + "\n")
    LOG_LINES.clear()
