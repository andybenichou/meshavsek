import os
from collections import defaultdict

import pandas as pd

from GuardsList import GuardsList
from helper import find_guard_slot


def find_guards(watch_list, guards_list: GuardsList, days, day, hour, spot,
                row, print_missing_names=True):
    missing_names = list()
    # First hour of the slot
    if pd.notna(row[spot]):
        found_guards = row[spot].split('\n')

        for g in found_guards:
            stripped_g = g.strip()
            if stripped_g in guards_list:
                guard = guards_list.find(stripped_g)
                if guard:
                    guard.last_spot = spot

                guards_list.remove(guard)
                guards_list.append(guard)

            elif stripped_g and stripped_g not in missing_names:
                missing_names.append(stripped_g)

        guards = GuardsList([guards_list.find(g.strip())
                             for g in row[spot].split('\n')])
        return guards

    # Find in already filled hours of the slot
    slot = find_guard_slot(day, hour, spot, days)

    if slot:
        guards_slot = watch_list[slot['start']['day']][slot['start']['hour']][spot]

        if guards_slot:
            return guards_slot

    if print_missing_names:
        if missing_names:
            print('\nNot known guards in previous guards file:')

        for name in missing_names:
            print(name)

        if missing_names:
            print()

    return GuardsList()


def get_days(df):
    days = list()
    last_day = None
    for index, row in df.iterrows():
        day = row['יום']

        if pd.notna(row['יום']):
            last_day = day

        if last_day not in days and pd.notna(row['ש.ג.']):
            days.append(last_day)

    return days


def get_previous_data(file_name, watch_list, guards_list: GuardsList,
                      guard_spots, print_missing_names=True):
    # Load the spreadsheet
    file_path = f'{file_name}.xlsx'
    src_previous_dir = os.path.dirname(os.path.abspath(__file__))
    previous_dir = os.path.join(src_previous_dir, file_path)

    if not os.path.exists(previous_dir):
        return watch_list

    xl = pd.ExcelFile(file_path)

    # Extract data from the first sheet (adjust as needed)
    df = xl.parse(xl.sheet_names[0])

    days = get_days(df)

    for d in days:
        watch_list[d] = defaultdict(lambda: defaultdict(list))

    # Iterate through the rows
    day = None
    for index, row in df.iterrows():
        if (day is None or day != row['יום']) and pd.notna(row['יום']):
            day = row['יום']

        if day not in days:
            break

        if isinstance(row['שעה'], str):
            hour = int(row['שעה'][:2])
        else:
            hour = int(row['שעה'].strftime('%H'))

        for p in guard_spots.keys():
            guards = find_guards(watch_list, guards_list, days, day,
                                 hour, p, row, print_missing_names)

            watch_list[day][hour][p] = guards

    return watch_list
