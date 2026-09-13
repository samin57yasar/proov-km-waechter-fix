# fleet_utils.py
# Catch-all helpers since 2013. Modernised style in 2026.

# Fixed 2026: the old value (1.609) was km-per-mile, not miles-per-km — the reciprocal.
# Every UK partner mileage figure was overstated by ~2.59× for over a decade.
MILES_PER_KM = 0.621371


def km_to_miles(km: float) -> float:
    """Convert kilometres to miles. Used by the nightly UK partner report."""
    return km * MILES_PER_KM


def format_number(value: float) -> str:
    """Format a float to one decimal place."""
    return f"{value:.1f}"


def format_percent(value: float) -> str:
    """Format a float as a whole-number percentage string."""
    return f"{int(value)}%"


def mean(values: list) -> float:
    """Return the arithmetic mean of a list of numbers, or 0 if the list is empty."""
    total = 0.0
    count = 0
    for v in values:
        total += v
        count += 1
    if count == 0:
        return 0.0
    return total / count


def is_due(pct: float, threshold: float) -> bool:
    """Return True if pct has reached or exceeded the threshold."""
    return pct >= threshold


def parse_service_date(text: str):
    """Parse a DD.MM.YYYY date string into a (year, month, day) tuple, or None on bad input.

    Note: used for the old garage form (2014). The form no longer exists.
    """
    parts = text.split(".")
    if len(parts) != 3:
        return None
    return (int(parts[2]), int(parts[1]), int(parts[0]))


def chunk_list(items: list, size: int) -> list:
    """Split items into sub-lists of at most size elements.

    Note: no longer called from anywhere (copied from Stack Overflow in 2013).
    """
    chunks = []
    current = []
    for item in items:
        current.append(item)
        if len(current) == size:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return chunks
