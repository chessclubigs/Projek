from datetime import datetime, timezone, timedelta

def offset_time(time, offset_minutes):
    return time - timedelta(minutes=offset_minutes)

def get_time_control_format(seconds, increment):
    remaining_hours = int(seconds / 3600)
    remaining_minutes = int(seconds / 60) % 60
    remaining_seconds = seconds % 60

    if remaining_hours == 0 and remaining_seconds == 0:
        return f"{remaining_minutes} | {increment}"
    if seconds < 3600:
        return f"{remaining_minutes}:{remaining_seconds:02} | {increment}"
    return f"{remaining_hours}:{remaining_minutes:02}:{remaining_seconds:02} | {increment}"


def get_time_control_type(seconds):
    if seconds < 3 * 60:
        return "Bullet"
    if seconds < 15 * 60:
        return "Blitz"
    if seconds < 60 * 60:
        return "Rapid"
    return "Classical"

def get_time_elapsed(time):
    cur_time = datetime.now(timezone.utc)
    offset_aware_time = time.replace(tzinfo=timezone.utc)

    return cur_time - offset_aware_time

def format_time_delta_hours(time_delta):
    hours = 24 * time_delta.days + int(time_delta.seconds / 3600)
    minutes = int(time_delta.seconds / 60) % 60
    seconds = time_delta.seconds % 60

    return f"{hours:02}:{minutes:02}:{seconds:02}"
