# km_wachter.py
# KM-Waechter decides when a Vossberg Mobility car needs a service.
# Written in 2013. Modernised style in 2026.

SERVICE_INTERVAL_KM = 15000
WARN_AT_PERCENT = 80


def wear_percent(km_since_service: float, interval: float) -> float:
    """Return the percentage of the service interval consumed (float, not floored)."""
    return (km_since_service / interval) * 100


def needs_service(car: dict) -> bool:
    """Return True if this car has consumed at least WARN_AT_PERCENT of its service interval."""
    last = car.get("last_service_km", 0)
    km_since = car.get("odometer", 0) - last
    return wear_percent(km_since, SERVICE_INTERVAL_KM) >= WARN_AT_PERCENT


def check_fleet(fleet: list) -> list:
    """Return the ids of every car that needs service, and print each one."""
    flagged = []
    for car in fleet:
        if needs_service(car):
            car_id = car.get("id", "<unknown>")
            flagged.append(car_id)
            print(f"SERVICE DUE: {car_id}")
    return flagged
