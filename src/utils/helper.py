from collections import defaultdict
from datetime import datetime, timedelta, time

from src.utils.consts import ENGLISH_WEEKDAY_TO_HEBREW


def get_day_of_week(date: datetime):
    if not isinstance(date, datetime):
        raise TypeError("Date must be a datetime object")

    # Get the name of the day of the week
    day_name = date.strftime("%A")

    return ENGLISH_WEEKDAY_TO_HEBREW[day_name]


def get_next_dates(days_number, date: datetime = None) -> [datetime]:
    if date:
        start = date
    else:
        start = get_day_at_midnight(datetime.now())

    dates = [start + timedelta(days=i) for i in range(days_number + 1)]

    return dates


def get_day_at_midnight(date: datetime):
    midnight_time = time(0, 0)
    # Combine today's date with the time set to midnight
    return datetime.combine(date, midnight_time)


def sort_watch_list(watch_list):
    # To sort it, you convert it to a list of items and sort by the key, which is the datetime
    sorted_watch_list = sorted(watch_list.items(), key=lambda item: item[0])

    # If you want to then convert it back to a defaultdict
    sorted_watch_list_dict = defaultdict(lambda: defaultdict(), {k: v for k, v in sorted_watch_list})

    return sorted_watch_list_dict
