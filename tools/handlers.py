from datetime import datetime, timezone


def get_current_time(**kwargs):
    """Return the current date and time in UTC."""
    now = datetime.now(timezone.utc)
    return {"current_time_utc": now.isoformat()}


def get_current_date(**kwargs):
    """Return the current date in ISO format in UTC."""
    now = datetime.now(timezone.utc)
    return {"current_date_utc": now.date().isoformat()}


def get_app_status(**kwargs):
    """Return a simple status payload for the app."""
    now = datetime.now(timezone.utc)
    return {
        "app_name": "Vincetoni-OS",
        "status": "online",
        "current_time_utc": now.isoformat(),
        "environment": "python"
    }