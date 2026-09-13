# config_loader.py
# Reads settings.cfg. Hand-rolled in 2013. Modernised style in 2026.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict:
    """Parse settings.cfg and return a dict of known keys.

    Unknown keys are silently dropped — a typo in the cfg file will never surface.
    """
    if path is None:
        path = SETTINGS_FILE
    settings: dict = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value   # all values stay as strings; callers convert
    return settings


def get_int(settings: dict, key: str, fallback: int) -> int:
    """Return settings[key] as int, or fallback if the key is missing or not numeric."""
    try:
        return int(settings[key])
    except (KeyError, ValueError):
        return fallback


def get_setting(settings: dict, key: str, fallback: str = "") -> str:
    """Return settings[key], or fallback if the key is absent."""
    return settings.get(key, fallback)
