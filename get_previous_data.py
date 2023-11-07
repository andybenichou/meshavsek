import os
import re
from collections import defaultdict

import pandas as pd

from GuardsList import GuardsList
from helper import find_guard_slot


def find_guards(watch_list, guards_list: GuardsList, date, spot, row,
                print_missing_names=True):
    missing_names = list()

    slot = find_guard_slot(date, spot)

    if not slot:
        return GuardsList()

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
    if slot:
        guards_slot = watch_list[slot['start']][spot]

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


def get_kitat_konenout(row, last_kitat_konenout):
    kitat_konenout = row['כתת כוננות']

    if pd.notna(kitat_konenout):
        # Search for the pattern: the word "חדר" followed by a space and one or more digits
        match = re.search(r"(\d+)", kitat_konenout)

        # Extract the number if a match is found
        room_number = int(match.group(1)) if match else None
        return room_number

    return last_kitat_konenout


def get_duty_room(row):
    for value in row:
        if pd.notna(value) and isinstance(value, str) and 'תורני רס"פ' in value:
            # Search for the pattern: the word "חדר" followed by a space and one or more digits
            match = re.search(r"(\d+)", value)

            # Extract the number if a match is found
            room_number = int(match.group(1)) if match else None

            return room_number

    return None


def parse_date(row):
    if pd.notna(row['יום']):
        return row['יום'].to_pydatetime()
    return None


def get_dates(df):
    dates = list()
    last_date = None
    for index, row in df.iterrows():
        date = parse_date(row)
        if date:
            last_date = date

        if last_date not in dates and pd.notna(row['ש.ג.']):
            dates.append(last_date)

    return dates


def get_previous_data(file_name, watch_list, guards_list: GuardsList,
                      guard_spots, print_missing_names=True):
    # Load the spreadsheet
    file_path = f'{file_name}.xlsx'
    src_previous_dir = os.path.dirname(os.path.abspath(__file__))
    previous_dir = os.path.join(src_previous_dir, file_path)

    duty_room_per_date = defaultdict(int)
    kitot_konenout = defaultdict(int)

    if not os.path.exists(previous_dir):
        return watch_list, duty_room_per_date, kitot_konenout

    xl = pd.ExcelFile(file_path)

    # Extract data from the first sheet (adjust as needed)
    df = xl.parse(xl.sheet_names[0])

    # Iterate through the rows
    date = None
    kitat_konenout = None
    for index, row in df.iterrows():
        buff_date = parse_date(row)
        if date is None or buff_date != date and buff_date:
            date = buff_date

            if date not in duty_room_per_date:
                duty_room = get_duty_room(row)

                if duty_room is not None:
                    duty_room_per_date[date] = duty_room

        if isinstance(row['שעה'], str):
            hour = int(row['שעה'][:2])
        else:
            hour = int(row['שעה'].strftime('%H'))

        date = date.replace(hour=hour)

        kitat_konenout = get_kitat_konenout(row, kitat_konenout)
        kitot_konenout[date] = kitat_konenout if kitat_konenout is not None else ''

        for p in guard_spots.keys():
            guards = find_guards(watch_list, guards_list, date, p, row,
                                 print_missing_names)
            watch_list[date][p] = guards

        watch_list[date]['כתת כוננות'] = kitat_konenout

    return watch_list, duty_room_per_date, kitot_konenout
