from datetime import datetime, timedelta

from consts import WEEK_DAYS, GUARD_SPOTS, ENGLISH_DAY_TO_HEBREW


def get_prec_day(day, days):
    day_i = days.index(day)
    prec_day = None

    if day_i > 0:
        prec_day = days[day_i - 1]

    return prec_day


def get_next_day(day, days):
    day_i = days.index(day)
    next_day = None

    if day_i < len(days):
        next_day = days[day_i + 1]

    return next_day


def get_next_week_day(day):
    day_i = WEEK_DAYS.index(day)

    return WEEK_DAYS[(day_i + 1) % 7]


def get_prec_week_day(day):
    day_i = WEEK_DAYS.index(day)

    return WEEK_DAYS[(day_i - 1) % 7]


def get_day_of_week(date):
    if not isinstance(date, datetime):
        raise TypeError("Date must be a datetime object")

    # Get the name of the day of the week
    day_name = date.strftime("%A")

    return ENGLISH_DAY_TO_HEBREW[day_name]


def get_next_dates(days_number, day=None):
    # Use the provided day or default to today
    if day:
        start = day
    else:
        start = datetime.now()

    # Generate the dates for 7 days starting from the base_date
    dates = [(start + timedelta(days=i)).date() for i in range(days_number)]

    return dates


def find_guard_slot(day, hour, spot, days):
    # Check if the guard already in another spot
    guard_spot = GUARD_SPOTS[spot]
    t = guard_spot['start']
    duration = 0
    slot_start_day = day
    while duration < guard_spot['duration']:
        slot_start_hour, slot_end_hour = t, (t + guard_spot['guard_duration']) % 24
        t = (t + guard_spot['guard_duration']) % 24
        duration += guard_spot['guard_duration']

        if slot_end_hour < slot_start_hour:
            slot_end_hour += 24

        if slot_start_hour <= hour + 24 < slot_end_hour:
            hour += 24
            slot_start_day = get_prec_day(day, days)

            if not slot_start_day:
                return None

        if slot_start_hour <= hour < slot_end_hour:
            return {
                'start': {
                    'day': slot_start_day,
                    'hour': slot_start_hour,
                },
                'end': {
                    'day': day,
                    'hour': slot_end_hour % 24,
                }
            }

    return None
