from datetime import datetime, timedelta


def add_seconds_to_datetime_now(seconds):
    """Add seconds to current timestamp and return it."""
    future_date = datetime.now() + timedelta(seconds=seconds)

    return future_date.strftime('%H:%M %d-%m-%Y')
