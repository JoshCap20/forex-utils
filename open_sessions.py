from time import sleep
from datetime import datetime, time, timedelta, timezone

UPDATE_INTERVAL: int = 60 * 5  # 5 minutes
TIMEZONE: timezone = timezone(timedelta(hours=-5))  # Eastern Time (-5) by default

SessionTimes = dict[str, dict[str, time]]

FOREX_SESSIONS: SessionTimes = {
    # Session times are in UTC
    "New York": {"open": time(13, 0), "close": time(22, 0)},
    "Tokyo": {"open": time(0, 0), "close": time(9, 0)},
    "Sydney": {"open": time(21, 0), "close": time(6, 0)},
    "London": {"open": time(7, 0), "close": time(16, 0)},
}


def convert_time_to_timezone(naive_time: time, current_datetime: datetime) -> str:
    """Convert a naive time object to a string representing the timezone identified above."""
    utc_datetime: datetime = datetime.combine(
        current_datetime.date(), naive_time, tzinfo=timezone.utc
    )
    target_datetime: datetime = utc_datetime.astimezone(TIMEZONE)
    return target_datetime.strftime("%I:%M %p")


def is_weekend_closure(current_datetime: datetime) -> bool:
    """Check if the current time is within the weekend closure period."""
    utc_datetime: datetime = current_datetime.astimezone(timezone.utc)
    week_day: int = utc_datetime.weekday()
    current_time: time = utc_datetime.time()
    return (week_day == 4 and current_time >= time(17, 0)) or (
        week_day == 6 and current_time < time(17, 0)
    )


def is_session_open(session_times: dict[str, time], current_datetime: datetime) -> bool:
    """Check if the session is currently open, considering the session's and current time's timezone."""
    # Convert session open/close times to current date and timezone for accurate comparison
    open_datetime: datetime = datetime.combine(
        current_datetime.date(), session_times["open"], tzinfo=timezone.utc
    ).astimezone(TIMEZONE)
    close_datetime: datetime = datetime.combine(
        current_datetime.date(), session_times["close"], tzinfo=timezone.utc
    ).astimezone(TIMEZONE)

    # Adjust for sessions that end the next day
    if session_times["close"] < session_times["open"]:
        close_datetime += timedelta(days=1)

    return open_datetime <= current_datetime < close_datetime


def get_time_details(session_times: dict[str, time], current_datetime: datetime) -> str:
    """Generate a string indicating how long until a session opens or closes."""
    now: datetime = current_datetime.astimezone(timezone.utc)
    today_open: datetime = datetime.combine(
        now.date(), session_times["open"], tzinfo=timezone.utc
    )
    today_close: datetime = datetime.combine(
        now.date(), session_times["close"], tzinfo=timezone.utc
    )

    # Adjust for sessions that end the next day
    if session_times["close"] < session_times["open"]:
        today_close += timedelta(days=1)  # Close time is on the next day

    if now < today_open:
        # Before session opens
        delta: timedelta = today_open - now
    elif today_open <= now < today_close:
        # During open session
        delta: timedelta = today_close - now
    else:
        # After session closes
        delta: timedelta = (today_open + timedelta(days=1)) - now  # Next opening time

    hours, remainder = divmod(delta.seconds, 3600)
    minutes = remainder // 60
    return f"{hours}h {minutes}m"


def get_session_details(sessions: SessionTimes, current_datetime: datetime) -> None:
    """Prints detailed information for all Forex sessions, including their open/close status and timings."""
    if is_weekend_closure(current_datetime):
        print("The Forex market is closed for the weekend.")
        return

    print(f"Current time: {current_datetime.strftime('%I:%M %p')}")
    for session_name, times in sessions.items():
        open_time_str: str = convert_time_to_timezone(times["open"], current_datetime)
        close_time_str: str = convert_time_to_timezone(times["close"], current_datetime)

        if is_session_open(times, current_datetime):
            status: str = "Open"
            time_detail: str = "closes in " + get_time_details(
                {"open": times["open"], "close": times["close"]}, current_datetime
            )
        else:
            status: str = "Closed"
            time_detail: str = "opens in " + get_time_details(
                {"open": times["open"], "close": times["close"]}, current_datetime
            )

        print(
            f"{session_name} Session ({open_time_str} to {close_time_str}): {status}, {time_detail}"
        )


if __name__ == "__main__":
    while True:
        current_local_datetime: datetime = datetime.now(tz=TIMEZONE)
        get_session_details(FOREX_SESSIONS, current_local_datetime)
        print("\nWaiting for next update...\n")
        sleep(UPDATE_INTERVAL)
