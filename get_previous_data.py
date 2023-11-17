import os
import re
from collections import defaultdict

import pandas as pd

from Guard import Guard
from GuardsList import GuardsList
from Room import Room
from consts import TORANOUT_PROPS, \
    DAY_COLUMN_NAME, HOUR_COLUMN_NAME, KITOT_KONENOUT_PROPS, \
    PREVIOUS_GUARD_SPOTS
from helper import find_guard_slot


def find_guards(watch_list, guards_list: GuardsList, date, spot, row,
                guards_spot, print_missing_names=True):
    missing_names = list()

    slot = find_guard_slot(guards_spot, date, spot)

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

        guards = list()
        for g in row[spot].split('\n'):
            found_g = guards_list.find(g.strip())
            if found_g:
                guards.append(found_g)
            elif g.strip():
                guards.append(Guard(g.strip(), last_name=''))

        return GuardsList(guards)

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

    if pd.notna(row[spot]):
        return row[spot]

    return GuardsList()


def get_kitat_konenout(row, last_kitat_konenout, last_kitat_konenout_duration):
    kitat_konenout = row[KITOT_KONENOUT_PROPS['column_name']]

    if pd.notna(kitat_konenout):
        # Search for the pattern: the word "חדר" followed by a space and one or more digits
        match = re.search(r"(\d+)", kitat_konenout)

        # Extract the number if a match is found
        room_number = int(match.group(1)) if match else None
        return room_number

    if last_kitat_konenout_duration < KITOT_KONENOUT_PROPS['duration']:
        return last_kitat_konenout

    return None


def get_duty_room(row, last_duty_room, date, rooms):
    if not TORANOUT_PROPS['start'] <= date.hour < TORANOUT_PROPS['end']:
        return None

    duty_room = row[TORANOUT_PROPS['column_name']]
    if pd.notna(duty_room):
        # Search for the pattern: the word "חדר" followed by a space and one or more digits
        match = re.search(r"(\d+)", duty_room)

        # Extract the number if a match is found
        room_number = int(match.group(1)) if match else ''

        for r in rooms:
            if r.number == room_number:
                return r

    return last_duty_room


def parse_date(row):
    if pd.notna(row[DAY_COLUMN_NAME]):
        return row[DAY_COLUMN_NAME].to_pydatetime()
    return None


def get_previous_data(file_name, watch_list, guards_list: GuardsList,
                      rooms: [Room], print_unknown_names=True):
    # Load the spreadsheet
    file_path = f'{file_name}.xlsx'
    src_previous_dir = os.path.dirname(os.path.abspath(__file__))
    previous_dir = os.path.join(src_previous_dir, file_path)

    duty_rooms = defaultdict(int)
    # kitot_konenout = defaultdict(int)

    if not os.path.exists(previous_dir):
        return watch_list, duty_rooms

    xl = pd.ExcelFile(file_path)

    # Extract data from the first sheet (adjust as needed)
    df = xl.parse(xl.sheet_names[0])

    # Iterate through the rows
    date = None
    duty_room = None
    guard_spots = list(filter(lambda key: key not in [DAY_COLUMN_NAME,
                                                      HOUR_COLUMN_NAME,
                                                      TORANOUT_PROPS['column_name'],
                                                      KITOT_KONENOUT_PROPS['column_name']],
                              df.columns))
    # last_kitat_konenout_duration = 0
    # last_kitat_konenout = None
    for index, row in df.iterrows():
        buff_date = parse_date(row)
        if date is None or buff_date != date and buff_date:
            date = buff_date

        if isinstance(row[HOUR_COLUMN_NAME], str):
            hour = int(row[HOUR_COLUMN_NAME][:2])
        else:
            hour = int(row[HOUR_COLUMN_NAME].strftime('%H'))

        date = date.replace(hour=hour)

        duty_room = get_duty_room(row, duty_room, date, rooms)
        duty_rooms[date] = duty_room

        # kitat_konenout = get_kitat_konenout(row, last_kitat_konenout, last_kitat_konenout_duration)
        # if kitat_konenout == last_kitat_konenout:
        #     last_kitat_konenout_duration += 1
        # else:
        #     last_kitat_konenout_duration = 1
        #     last_kitat_konenout = kitat_konenout
        #
        # kitot_konenout[date] = kitat_konenout if kitat_konenout is not None else ''

        for spot in guard_spots:
            guards = find_guards(watch_list, guards_list, date, spot, row,
                                 PREVIOUS_GUARD_SPOTS,
                                 print_missing_names=print_unknown_names)
            watch_list[date][spot] = guards

    return watch_list, duty_rooms
