from collections import defaultdict

import pandas as pd

from GuardsList import GuardsList


def find_guards(watch_list, guards_list_obj: GuardsList, guard_spots_prop,
                days, day_prop, hour_prop, spot_prop, row_prop,
                print_missing_names=True):
    # First hour of the slot
    if pd.notna(row_prop[spot_prop]):
        found_guards = row_prop[spot_prop].split('\n')

        for g in found_guards:
            stripped_g = g.strip()
            if stripped_g in guards_list_obj:
                guard_obj = guards_list_obj.find(stripped_g)
                guards_list_obj.remove(guard_obj)
                guards_list_obj.append(guard_obj)

            elif print_missing_names:
                print(stripped_g)

        guards = GuardsList([guards_list_obj.find(g.strip())
                             for g in row_prop[spot_prop].split('\n')])
        return guards

    # Find in already filled hours of the slot
    for slot in guard_spots_prop[spot_prop]:
        beginning_str, g_end_str = slot.split('-')
        beginning, g_end = map(int, [beginning_str[:2], g_end_str[:2]])

        if g_end < beginning:
            g_end += 24

            if beginning < hour_prop + 24 < g_end:
                hour_prop += 24

        if beginning <= hour_prop < g_end:
            for h in range(beginning, g_end):
                slot_d = day_prop
                if beginning < hour_prop < g_end:
                    if hour_prop >= 24:
                        day_i = days.index(day_prop)

                        if day_i > 0:
                            slot_d = days[day_i - 1]

                        else:
                            break

                guards_slot = watch_list[slot_d][f'{beginning:02d}00'][spot_prop]

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


def get_data(file_name, watch_list, guards_list_obj: GuardsList,
             guard_spots_prop, print_missing_names=True):
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

        hour_str = row['שעה'].strftime('%H%M')

        for p in guard_spots_prop.keys():
            guards = find_guards(watch_list, guards_list_obj,
                                 guard_spots_prop, days, day,
                                 int(hour_str[:2]), p, row,
                                 print_missing_names)

            watch_list[day][hour_str][p] = guards

    return watch_list
