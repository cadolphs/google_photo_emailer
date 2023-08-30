from datetime import datetime, timedelta, timezone


def get_tomorrows_date_string() -> str:
    return (datetime.now() + timedelta(days=1)).isoformat() + "Z"
