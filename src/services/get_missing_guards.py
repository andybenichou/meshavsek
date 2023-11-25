import os
import re
from datetime import datetime, timedelta

import pandas as pd

from guards_config import HAPAK_HOURS, HOME_HOURS
from guards_config import MISSING_GUARDS
from src.models.GuardsList import GuardsList
from src.utils.helper import get_next_dates, get_day_of_week, get_day_at_midnight


def complete_each_guard_missing_slots(missing_guards):
    for date, missing in missing_guards.items():
        weekday = get_day_of_week(date)
        for guard in missing:
            exit_hour = HOME_HOURS['exit']['regular'] \
                if not guard.is_living_far_away \
                else HOME_HOURS['exit']['far_away']
            return_hour = HOME_HOURS['return']['regular']['week_day'] \
                if not guard.is_living_far_away \
                else HOME_HOURS['return']['far_away']['week_day']

            if weekday == 'ו':
                return_hour = HOME_HOURS['return']['regular']['shabbat'] \
                    if not guard.is_living_far_away \
                    else HOME_HOURS['return']['far_away']['shabbat']

            time_obj = {
                'start': date.replace(hour=exit_hour),
                'end': (date + timedelta(days=1)).replace(hour=return_hour)
            }

            guard.add_not_available_time(time_obj['start'], time_obj['end'])


def get_missing_guards(file_name, sheet_name, guards: GuardsList,
                       days_input: int, print_unknown_guards=True):
    def is_valid_format(time_range):
        if not isinstance(time_range, str):
            return False

        # Regular expression pattern to match the formats "0-0" or "00-00"
        pattern = r'^\d{1,2}-\d{1,2}$'
        return bool(re.match(pattern, time_range))

    file_path = f'data/input/{file_name}.xlsx'
    ROOT_DIR = os.environ.get('ROOT_DIR')
    full_path = os.path.join(ROOT_DIR, file_path)

    if not os.path.exists(full_path):
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
            # Get custom missing hours
            if (date, 'מ12') in row:
                if pd.notna(row[(date, 'מ12')]) \
                        and is_valid_format(row[(date, 'מ12')]):
                    start_hour, end_hour = row[(date, 'מ12')].split('-')

                    if start_hour or end_hour:
                        start_hour = int(start_hour)
                        end_hour = int(end_hour)

                        if start_hour < end_hour:
                            end_date = date if end_hour < 24 else date + timedelta(days=1)
                            end_hour %= 24

                            time_obj = {
                                'start': date.replace(hour=start_hour),
                                'end': end_date.replace(hour=end_hour)
                            }

                            guard.add_not_available_time(time_obj['start'], time_obj['end'])

            next_date = pd.Timestamp(date + timedelta(days=1))
            if (next_date, 'עד 12') in row:
                if pd.isna(row[(next_date, 'עד 12')]) or not row[(next_date, 'עד 12')]:
                    is_guard_missing = True
                else:
                    is_guard_missing = False

                if guard in missing_guards[date] and not is_guard_missing:
                    missing_guards[date].remove(guard)

                elif guard not in missing_guards[date] and is_guard_missing:
                    missing_guards[date].append(guard)

                # Get HAPAK
                if row[(next_date, 'עד 12')] == "חפ''ק":
                    start_hapak = HAPAK_HOURS['start']['hour']
                    end_same_day = HAPAK_HOURS['end']['same_day']
                    end_hapak_hour = HAPAK_HOURS['end']['hour']

                    if end_same_day:
                        if end_hapak_hour <= start_hapak:
                            end_hapak_hour = start_hapak + 1

                    time_obj = {
                        'start': date.replace(hour=start_hapak),
                        'end': (
                                date + timedelta(days=0 if end_same_day else 1)
                            ).replace(hour=end_hapak_hour)
                    }

                    guard.add_not_available_time(time_obj['start'], time_obj['end'])

                elif guard not in missing_guards[date] and is_guard_missing:
                    missing_guards[date].append(guard)

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
