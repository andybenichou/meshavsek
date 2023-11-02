from collections import defaultdict

import pandas as pd

from GuardsList import GuardsList
from helper import find_guard_slot


def find_guards(watch_list, guards_list: GuardsList, days, day, hour, spot,
                row, print_missing_names=True):
    # First hour of the slot
    if pd.notna(row[spot]):
        found_guards = row[spot].split('\n')

        for g in found_guards:
            stripped_g = g.strip()
            if stripped_g in guards_list:
                guard_obj = guards_list.find(stripped_g)
                guards_list.remove(guard_obj)
                guards_list.append(guard_obj)

            elif print_missing_names and stripped_g:
                print(stripped_g)

        guards = GuardsList([guards_list.find(g.strip())
                             for g in row[spot].split('\n')])
        return guards

    # Find in already filled hours of the slot
    slot = find_guard_slot(day, hour, spot, days)

    if slot:
        guards_slot = watch_list[slot['start']['day']][slot['start']['hour']][spot]

        if guards_slot:
            return guards_slot

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
            hour = row['שעה'].strftime('%H%M')

        for p in guard_spots.keys():
            guards = find_guards(watch_list, guards_list, days, day,
                                 int(hour), p, row,
                                 print_missing_names)

            watch_list[day][hour][p] = guards

    return watch_list
