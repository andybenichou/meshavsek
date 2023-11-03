from datetime import datetime, timedelta

from consts import GUARD_SPOTS, WEEK_DAYS


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


def get_today_day_of_week():
    # Get the current date
    today = datetime.today()

    # Get the name of the day of the week
    day_name = today.strftime("%A")

    ENGLISH_DAY_TO_HEBREW = {
        'Sunday': 'א',
        'Monday': 'ב',
        'Tuesday': 'ג',
        'Wednesday': 'ד',
        'Thursday': 'ה',
        'Friday': 'ו',
        'Saturday': 'שבת',
    }

    return ENGLISH_DAY_TO_HEBREW[day_name]


def get_week_dates_hebrew(day=None):
    DAYS_IN_HEBREW = {
        6: "ראשון",
        0: "שני",
        1: "שלישי",
        2: "רביעי",
        3: "חמישי",
        4: "שישי",
        5: "שבת",
    }

    # Use the provided day or default to today
    if day:
        start_of_week = day
    else:
        start_of_week = datetime.now()

    # Generate the dates for 7 days starting from the base_date
    week_dates = [(start_of_week + timedelta(days=i)).date() for i in range(7)]

    # Format the dates and days into the desired format
    formatted_dates = [f"{DAYS_IN_HEBREW[date.weekday()]} {date.strftime('%d.%m')}" for date in week_dates]

    return formatted_dates


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
