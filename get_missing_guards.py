import os
from datetime import datetime, timedelta
from typing import Union

import pandas as pd

from Guard import Guard
from GuardsList import GuardsList
from consts import WEEK_DAYS
from helper import get_week_dates_hebrew, get_next_week_day


WEEKDAYS_FORMAT = {
    'ראשון': 'א',
    'שני': 'ב',
    'שלישי': 'ג',
    'רביעי': 'ד',
    'חמישי': 'ה',
    'שישי': 'ו',
    'שבת': 'שבת',
}


def merge_friday_saturday(date_str: str) -> str:
    # Split the string into day name and date
    day_name, dd_mm = date_str.split()

    # Validate day name
    if day_name not in ['שישי', 'שבת']:
        return "The day name is not Friday or Saturday."

    # Parse the date into a datetime object
    try:
        dd, mm = map(int, dd_mm.split('.'))
        # Assuming the year is the current year, which you may need to adjust
        current_year = datetime.now().year
        date_obj = datetime(current_year, mm, dd)

        # If the provided date is a Saturday, we subtract one day to get Friday
        if day_name == 'שבת':
            date_obj -= timedelta(days=1)

        # Format the Friday date
        friday_dd_mm = date_obj.strftime('%d.%m')

        # Return the combined string
        return f'שישי ושבת {friday_dd_mm}'

    except ValueError as e:
        return "Error in date format: " + str(e)


def find_guard(guards: GuardsList, guard_name) -> Union[Guard, None]:
    for g in guards:
        if g.name in guard_name:
            return g

    return None


def get_missing_guards(file_name, guards: GuardsList):
    # Load the spreadsheet
    file_path = f'{file_name}.xlsx'
    src_missing_dir = os.path.dirname(os.path.abspath(__file__))
    missing_dir = os.path.join(src_missing_dir, file_path)

    if not os.path.exists(missing_dir):
        return {day: list() for day in WEEK_DAYS}

    xl = pd.ExcelFile(file_path)

    # Extract data from the first sheet (adjust as needed)
    df = xl.parse(xl.sheet_names[0])

    curr_week_days = get_week_dates_hebrew(datetime.now() - timedelta(days=1))

    not_known_guards = list()
    missing_guards = {date: list() for date in curr_week_days}
    for index, row in df.iterrows():
        for date in missing_guards:
            date_key = date
            if 'שישי' in date or 'שבת' in date:
                date = merge_friday_saturday(date)

            if date in row and pd.notna(row[date]) \
                    and row[date] not in missing_guards[date_key]:
                guard_str = row[date]
                guard = find_guard(guards, guard_str)
                formatted_day = WEEKDAYS_FORMAT[date_key.split()[0]]

                if not guard:
                    if guard_str not in not_known_guards:
                        not_known_guards.append(guard_str)

                    missing_guards[date_key].append(guard_str)
                    continue

                if guard.is_living_far_away:
                    time_obj = {
                        'start': {'day': formatted_day, 'hour': 6},
                        'end': {'day': get_next_week_day(formatted_day), 'hour': 16}
                    }
                else:
                    time_obj = {
                        'start': {'day': formatted_day, 'hour': 9},
                        'end': {'day': get_next_week_day(formatted_day), 'hour': 12}
                    }

                guard.add_not_available_time(time_obj['start'], time_obj['end'])

                missing_guards[date_key].append(guard)

    formatted_missing_guards = dict()
    for date, missing in missing_guards.items():
        weekday = WEEKDAYS_FORMAT[date.split()[0]]
        formatted_missing_guards[weekday] = missing

    if not_known_guards:
        print('\nNot known guards in missing guards file:')

    for guard in not_known_guards:
        print(guard)

    if not_known_guards:
        print()

    return formatted_missing_guards
