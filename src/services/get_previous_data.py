# Copyright (c) 2023, Andy Benichou
# All rights reserved.
#
# This file is part of a software project governed by the Custom License
# for Private Use.
# Redistribution and use in source and binary forms, with or
# without modification, are not permitted for any non-commercial or
# commercial purposes without prior written permission from the owner.
#
# This software is provided "as is", without warranty of any kind,
# express or implied.
# In no event shall the authors be liable for any claim, damages,
# or other liability.
#
# For full license terms, see the LICENSE file in the project root
# or contact Andy Benichou.
#
# Get previous data file of the project Meshavshek


import os
import re
from collections import defaultdict

import pandas as pd

from config import DAY_COLUMN_NAME, HOUR_COLUMN_NAME
from guards_config import KITOT_KONENOUT_PROPS, TORANOUT_PROPS, \
    PREVIOUS_GUARD_SPOTS
from src.models.Guard import Guard
from src.models.GuardsList import GuardsList
from src.models.Room import Room


def find_guards(watch_list, guards_list: GuardsList, date, spot, row,
                missing_names):
    slot = spot.find_guard_slot(date)

    # First hour of the slot
    if pd.notna(row[spot.name]):
        found_guards = row[spot.name].split('\n')

        for g in found_guards:
            stripped_g = g.strip()
            if stripped_g in guards_list:
                guard = guards_list.find(stripped_g)
                if guard:
                    guard.last_spot = spot

                    guards_list.remove(guard)
                    guards_list.append(guard)

            elif stripped_g and stripped_g not in missing_names \
                    and stripped_g != 'None':
                missing_names.append(stripped_g)

        guards = list()
        for g in row[spot.name].split('\n'):
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

    if pd.notna(row[spot.name]):
        return row[spot.name]

    return GuardsList()


def get_kitat_konenout(row, last_kitat_konenout, last_kitat_konenout_duration):
    if KITOT_KONENOUT_PROPS['column_name'] not in row:
        if last_kitat_konenout:
            kitat_konenout = last_kitat_konenout
        else:
            return None
    else:
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
    if not TORANOUT_PROPS['start'] <= date.hour < TORANOUT_PROPS['end'] \
            or TORANOUT_PROPS['column_name'] not in row:
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
    file_path = f'data/input/{file_name}.xlsx'

    ROOT_DIR = os.environ.get('ROOT_DIR')
    full_path = os.path.join(ROOT_DIR, file_path)

    duty_rooms = defaultdict(int)
    kitot_konenout = defaultdict(int)

    if not os.path.exists(full_path):
        return watch_list, duty_rooms, kitot_konenout

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

    missing_names = list()
    last_kitat_konenout_duration = 0
    last_kitat_konenout = None
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

        kitat_konenout = get_kitat_konenout(row, last_kitat_konenout, last_kitat_konenout_duration)
        if kitat_konenout == last_kitat_konenout:
            last_kitat_konenout_duration += 1
        else:
            last_kitat_konenout_duration = 1
            last_kitat_konenout = kitat_konenout

        kitot_konenout[date] = kitat_konenout if kitat_konenout is not None else ''

        for spot in guard_spots:
            spot_obj = list(filter(lambda s: s.name == spot, PREVIOUS_GUARD_SPOTS))[0]
            guards = find_guards(watch_list, guards_list, date, spot_obj, row,
                                 missing_names)
            watch_list[date][spot_obj] = guards

    if print_unknown_names:
        if missing_names:
            print('\nNot known guards in previous guards file:')

        for name in missing_names:
            print(name)

        if missing_names:
            print()

    return watch_list, duty_rooms, kitot_konenout
