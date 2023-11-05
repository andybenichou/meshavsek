import os
from collections import defaultdict
from datetime import datetime, timedelta

import pandas as pd

from GuardsList import GuardsList
from guards_properties import MISSING_GUARDS
from helper import get_next_dates, get_next_week_day, get_day_of_week


def complete_each_guard_missing_slots(missing_guards):
    for date, missing in missing_guards.items():
        weekday = get_day_of_week(date)
        for guard in missing:
            exit_hour = 12 if not guard.is_living_far_away else 8
            return_hour = 12 if not guard.is_living_far_away else 16

            if weekday == 'שישי':
                return_hour = 21 if not guard.is_living_far_away else 23

            time_obj = {
                'start': {'day': weekday, 'hour': exit_hour},
                'end': {'day': get_next_week_day(weekday), 'hour': return_hour}
            }

            guard.add_not_available_time(time_obj['start'], time_obj['end'])


def get_missing_guards(file_name, sheet_name, guards: GuardsList):
    file_path = f'{file_name}.xlsx'
    src_missing_dir = os.path.dirname(os.path.abspath(__file__))
    missing_dir = os.path.join(src_missing_dir, file_path)

    if not os.path.exists(missing_dir):
        missing_guards = MISSING_GUARDS
        complete_each_guard_missing_slots(missing_guards)
        return missing_guards

    xl = pd.ExcelFile(file_path)
    df = xl.parse(sheet_name, header=[0, 2])

    next_dates = get_next_dates(7, datetime.now() - timedelta(days=1))
    not_known_guards = list()
    missing_guards = {pd.Timestamp(date): list()
                      for date in next_dates}
    for index, row in df.iterrows():
        # Obtain the first_name and last_name values as scalars
        first_name = row[('שם פרטי', 'Unnamed: 0_level_1')]
        last_name = row[('שם משפחה', 'נוכחות:')]

        # Check if the values are not NaN
        if pd.isna(first_name) or pd.isna(last_name):
            continue  # Skip to the next row if either is NaN

        # Convert to string and strip any whitespace
        first_name = str(first_name).strip()
        last_name = str(last_name).strip()

        guard_str = f'{first_name} {last_name}'
        guard = guards.find(guard_str)

        if not guard:
            not_known_guards.append(guard_str)
            continue

        for date in missing_guards:
            next_day = date + pd.Timedelta(days=1)

            if (next_day, 'עד 12') in row:
                is_guard_missing = False if row[(next_day, 'עד 12')] == 1 else True
                if guard in missing_guards[date] and not is_guard_missing:
                    missing_guards[date].remove(guard)

                elif guard not in missing_guards[date] and is_guard_missing:
                    missing_guards[date].append(guard)

    formatted_missing_guards = dict()
    for date, missing in missing_guards.items():
        # If almost all the guards absent, there must be an error in the xlsx file
        if len(missing) >= 0.9 * len(guards):
            missing = list()
            missing_guards[date] = missing

        weekday = get_day_of_week(date)
        formatted_missing_guards[weekday] = missing

    complete_each_guard_missing_slots(missing_guards)

    if not_known_guards:
        print('\nNot known guards in missing guards file:')

    for guard in not_known_guards:
        print(guard)

    if not_known_guards:
        print()

    return formatted_missing_guards
