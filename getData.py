from collections import defaultdict

import pandas as pd


def find_guards(watch_list, guards_list_prop, guard_spots_prop, days,
                day_prop, hour_prop, spot_prop, row_prop):
    # First hour of the slot
    if pd.notna(row_prop[spot_prop]):
        found_guards = row_prop[spot_prop].split('\n')

        for g in found_guards:
            stripped_g = g.strip()
            if stripped_g in guards_list_prop:
                guards_list_prop.remove(stripped_g)
                guards_list_prop.append(stripped_g)

            else:
                print(stripped_g)

        return row_prop[spot_prop].split('\n')

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

                        if day_i < len(days) - 1:
                            slot_d = days[day_i + 1]

                        else:
                            break

                guards_slot = watch_list[slot_d][f'{h % 24:02d}00'][spot_prop]

                if guards_slot:
                    return guards_slot

    return list()


def get_days(df):
    days = list()
    last_day = None
    for index, row in df.iterrows():
        day = row['Day']
        hour_str = row['Hour'].strftime('%H%M')

        if pd.notna(row['Day']):
            last_day = day

        if last_day not in days \
                and hour_str == '0200' and pd.notna(row['Entrance']):
            days.append(last_day)

    return days


def get_data(file_name, watch_list, guards_list_prop, guard_spots_prop):
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
        if (day is None or day != row['Day']) and pd.notna(row['Day']):
            day = row['Day']

        if day not in days:
            break

        hour_str = row['Hour'].strftime('%H%M')

        for p in guard_spots_prop.keys():
            guards = find_guards(watch_list, guards_list_prop,
                                 guard_spots_prop, days, day,
                                 int(hour_str[:2]), p, row)

            watch_list[day][hour_str][p] = guards

    return watch_list
