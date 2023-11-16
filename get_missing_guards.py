import os
from datetime import datetime, timedelta

import pandas as pd

from GuardsList import GuardsList
from guards_properties import MISSING_GUARDS
from helper import get_next_dates, get_day_of_week, get_day_at_midnight


def complete_each_guard_missing_slots(missing_guards):
    for date, missing in missing_guards.items():
        weekday = get_day_of_week(date)
        for guard in missing:
            exit_hour = 12 if not guard.is_living_far_away else 10
            return_hour = 12 if not guard.is_living_far_away else 16

            if weekday == 'ו':
                return_hour = 21 if not guard.is_living_far_away else 23

            time_obj = {
                'start': date.replace(hour=exit_hour),
                'end': (date + timedelta(days=1)).replace(hour=return_hour)
            }

            guard.add_not_available_time(time_obj['start'], time_obj['end'])


def get_missing_guards(file_name, sheet_name, guards: GuardsList,
                       days_input: int, print_unknown_guards=True):
    file_path = f'{file_name}.xlsx'
    src_missing_dir = os.path.dirname(os.path.abspath(__file__))
    missing_dir = os.path.join(src_missing_dir, file_path)

    if not os.path.exists(missing_dir):
        missing_guards = MISSING_GUARDS
        complete_each_guard_missing_slots(missing_guards)
        return missing_guards

    xl = pd.ExcelFile(file_path)
    df = xl.parse(sheet_name, header=[0, 2])

    next_dates = get_next_dates(days_input + 2,
                                get_day_at_midnight(datetime.now()) - timedelta(days=1))

    not_known_guards = list()
    missing_guards = {date: list() for date in next_dates}
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
            next_date = pd.Timestamp(date + timedelta(days=1))

            if (next_date, 'עד 12') in row:
                if row[(next_date, 'עד 12')] == 1 or row[(next_date, 'עד 12')] == 'חפ״ק':
                    is_guard_missing = False
                else:
                    is_guard_missing = True

                if guard in missing_guards[date] and not is_guard_missing:
                    missing_guards[date].remove(guard)

                elif guard not in missing_guards[date] and is_guard_missing:
                    missing_guards[date].append(guard)

                if row[(next_date, 'עד 12')] == "חפ''ק":
                    time_obj = {
                        'start': date.replace(hour=12),
                        'end': (date + timedelta(days=1)).replace(hour=12)
                    }

                    guard.add_not_available_time(time_obj['start'], time_obj['end'])

    filtered_missing_guards = dict()
    for date, missing in missing_guards.items():
        # If almost all the guards absent, there must be an error in the xlsx file
        if len(missing) >= 0.9 * len(guards):
            filtered_missing_guards[date] = list()
        else:
            filtered_missing_guards[date] = missing

    complete_each_guard_missing_slots(filtered_missing_guards)

    if print_unknown_guards:
        if not_known_guards:
            print('\nNot known guards in missing guards file:')

        for guard in not_known_guards:
            print(guard)

        if not_known_guards:
            print()

    return filtered_missing_guards
