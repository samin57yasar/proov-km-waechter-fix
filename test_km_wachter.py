# test_km_wachter.py
from km_wachter import needs_service, wear_percent


def test_almost_due_car_is_flagged():
    # A car at 14,900 of its 15,000 km window is about 99% worn and MUST be flagged.
    assert needs_service({"id": "VOS-4471", "odometer": 14900, "last_service_km": 0}) is True


def test_missing_reading_is_not_treated_as_zero():
    # A car with NO last-service reading must not be treated as fully worn.
    assert needs_service({"id": "VOS-7788", "odometer": 92000}) is False


def test_wear_percent_at_exactly_80():
    # 12,000 km driven out of a 15,000 km interval is exactly 80% — right on the warning boundary.
    assert wear_percent(12000, 15000) == 80.0
