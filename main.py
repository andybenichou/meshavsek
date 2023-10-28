import csv
from collections import defaultdict
from itertools import cycle

from openpyxl import load_workbook
from openpyxl.styles import Alignment
from getData import getData

import pandas as pd


# Define the guard points and their time slots
guard_points = {
    'Entrance': ['0200-0500', '0500-0800', '0800-1100', '1100-1400',
                 '1400-1700', '1700-2000', '2000-2300', '2300-0200'],
    'Rear': ['0200-0500', '0500-0800', '0800-1100', '1100-1400', '1400-1700',
             '1700-2000', '2000-2300', '2300-0200'],
    'Penthouse': ['0200-0500', '0500-0800', '0800-1100', '1100-1400',
                  '1400-1700', '1700-2000', '2000-2300', '2300-0200'],
    'East': ['2000-2300', '2300-0200', '0200-0500', '0500-0800'],
    'Patrol': ['2200-0200', '0200-0600'],
}

# List of guards
guards_list = ['Andy', 'Saspo', 'David', 'Sauveur', 'Lotem', 'Enzo',
               'Benichou', 'Guetta', 'סיני', 'רווה', 'דוד', 'אנדי', 'אגומס', 'שמעון', 'דובר',
               'כלפה', 'ליאור', 'אנזו', 'דורון', 'משה', 'משה החופל', 'אסף',
               'ארד', 'אלכסיי', 'ניסנוב', 'עמיחי', 'לוטם', 'שגיא', 'נפמן',
               'סדון', 'מטמוני', 'דימנטמן', 'לואיס', 'אבנר', 'יונג', 'כהן',
               'דותן', 'Sinai', 'Yoni', 'Noe', 'Ben', 'Daboush',
               'Dael', 'Moshe', 'Alex', 'Noa', 'Alisa', 'Dana', 'Attia', 'Dan',
               'Elliot', 'Ilan', 'Lea', 'Celine', 'Jason', 'Leon', 'Shana',
               'Helena', 'Jeremy', 'Yoel', 'Leo', 'Yona', 'Serguei', 'Alexei',
               'Nora', 'Sanson', 'Serge', 'Solal', 'Elsa', 'Carla']

# List of duos
duos = [('Andy', 'Saspo')]

# List of missing guards each day
missings = {
    'Sunday': ['Guetta'],
    'Monday': ['Solal'],
    'Tuesday': ['Elsa'],
    'Wednesday': list(),
    'Thursday': list(),
    'Friday': list(),
    'Saturday': list()
}

# Define the days
week_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']


# Helper function to check if a guard is available
def is_guard_available(watch_list, guard, day_prop, time_prop, days_prop):
    day_i = days_prop.index(day_prop)
    prec_day = None
    hour = int(time_prop[:2])

    # Check if in missings guards
    if day_i > 0:
        prec_day = days_prop[day_i - 1]

    if (guard in missings[day_prop] and hour >= 12) or \
            (prec_day and
             guard in missings[prec_day] and
             hour <= 14):
        return False

    # Check if the guard already in another point
    for p in guard_points:
        for t in guard_points[p]:
            beginning_str, g_end_str = t.split('-')
            beginning, g_end = map(int, [beginning_str[:2], g_end_str[:2]])

            if g_end < beginning:
                g_end += 24

                if beginning < hour + 24 < g_end:
                    hour += 24

            slot_d = day_prop
            if beginning < hour < g_end:
                if hour == 24:
                    day_i = days_prop.index(day_prop)

                    if day_i > 0:
                        slot_d = days_prop[day_i - 1]

            if beginning <= hour < g_end and \
                    guard in watch_list[slot_d][beginning_str][p]:
                return False

    return True


# Helper function to get the next available guard
def get_next_available_guard(watch_list, guard_cycle_prop, used_guards_prop,
                             day_prop, time_prop, days_prop, current_guard=None):
    if current_guard is not None:
        index = guards_list.index(current_guard)
        buff_cycle = cycle(guards_list[index:] + guards_list[:index])
    else:
        buff_cycle = guard_cycle_prop

    while True:
        guard = next(buff_cycle)
        if guard not in used_guards_prop \
                and is_guard_available(watch_list, guard, day_prop, time_prop, days_prop):
            duo = next((d for d in duos if guard in d), None)
            if duo:
                partner = duo[0] if duo[1] == guard else duo[1]
                if current_guard:
                    continue

                elif partner not in used_guards_prop \
                        and is_guard_available(watch_list, partner, day_prop, time_prop, days_prop):
                    return guard, partner
            else:
                return guard, None


def getDays(watch_list):
    days_num = input("How many days do you need to schedule?")
    # days_num = 3
    days_list = list()
    last_day = None

    for day in list(watch_list.keys()):
        for time in sorted(set([f'{hour:02d}00' for hour in range(24)])):
            for point in guard_points:
                if watch_list[day][time][point]:
                    last_day = day
                    break

        if last_day == day:
            continue

    days_list.append(last_day)

    days_cycle = cycle(week_days)
    day = next(days_cycle)
    while last_day != day:
        day = next(days_cycle)

    for _ in range(days_num):
        day = next(days_cycle)
        days_list.append(day)

    return days_list


def getWatchListData(watch_list, days_prop):
    # Assign guards to each slot
    guard_cycle = cycle(guards_list)
    for day in days_prop:
        for time in sorted(set([f'{hour:02d}00' for hour in range(24)])):
            hour = int(time[:2])

            if (days_prop.index(day) == 0 and hour < 2) or \
                    (days_prop.index(day) == len(days_prop) - 1 and hour >= 20):
                continue

            used_guards = []
            for point in guard_points:
                if watch_list[day][time][point]:
                    continue

                guards = None

                need_guard_point = False
                for slot in guard_points[point]:
                    start_str, end_str = slot.split('-')
                    start, end = int(start_str[:2]), int(end_str[:2])

                    if end < start:
                        end += 24

                        if start < hour + 24 < end:
                            hour += 24

                    if start <= hour < end:
                        need_guard_point = True

                    if start < hour < end:
                        slot_day = day
                        if hour == 24:
                            day_index = days_prop.index(day)

                            if day_index > 0:
                                slot_day = days_prop[day_index - 1]

                        guards = \
                            watch_list[slot_day][f'{((hour - 1) % 24):02d}00'][
                                point]

                if not guards and need_guard_point:
                    guard1, guard2 = get_next_available_guard(watch_list,
                                                              guard_cycle,
                                                              used_guards,
                                                              day,
                                                              time,
                                                              days_prop)
                    used_guards.extend([g for g in (guard1, guard2) if g])

                    if guard2 is None:
                        guard2 = get_next_available_guard(watch_list,
                                                          guard_cycle,
                                                          used_guards,
                                                          day,
                                                          time,
                                                          days_prop,
                                                          current_guard=guard1)[0]

                        used_guards.append(guard2)

                    guards = [guard1, guard2]

                if guards:
                    watch_list[day][time][point].extend(guards)

    return watch_list


def exportToCSV(watch_list, days_prop):
    with open('watch_list.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ['Day', 'Time', 'Entrance', 'Penthouse', 'Rear', 'East', 'Patrol']
        csvwriter.writerow(header)
        for day in days_prop:
            for hour in range(24):
                time = f'{hour:02d}00'
                row = [day, time]

                for point in guard_points.keys():
                    guards_str = '\n'.join(watch_list[day][time][point]) \
                        if watch_list[day][time][point] else ' '
                    row.append(guards_str)
                csvwriter.writerow(row)


def getExcelDataFrame(watch_list, days_prop):
    columns = ['Day', 'Time'] + list(guard_points.keys())
    data = list()

    for day in days_prop:
        for hour in range(24):
            if (days_prop.index(day) == 0 and hour < 2) or (
                    days_prop.index(day) == len(days_prop) - 1 and hour >= 20):
                continue

            time = f'{hour:02d}00'
            time_for_excel = f'{hour:02d}:00'  # formatted for Excel
            row = [day, time_for_excel]

            for point in guard_points.keys():
                guards_str = '\n'.join(watch_list[day][time][point]) if \
                    watch_list[day][time][point] else ' '
                row.append(guards_str)
            data.append(row)

    return pd.DataFrame(data, columns=columns)


def formatExcel(df, worksheet):
    # Merge adjacent cells with the same content
    for col_num in range(1, len(df.columns) + 2):
        start_row = 1
        start_content = None

        for row_num in range(1, len(df) + 2):
            content = worksheet.cell(row=row_num, column=col_num).value

            if start_content is None:
                start_content = content

            elif content != start_content or row_num == len(df) + 1:
                if start_row < row_num - 1:
                    end_row = row_num - 1 if row_num < len(df) + 1 else row_num
                    worksheet.merge_cells(start_row=start_row,
                                          start_column=col_num,
                                          end_row=end_row, end_column=col_num)

                if row_num < len(df) + 1:
                    start_row = row_num
                    start_content = content

    # Adjust the column width according to content, wrap text, and center align text
    for col in worksheet.columns:
        max_length = 0
        column = [cell for cell in col]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
                cell.alignment = Alignment(wrap_text=True, horizontal='center',
                                           vertical='center')  # Set wrap text and center alignment
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width


def exportToExcel(file_name, watch_list, days_prop):
    df = getExcelDataFrame(watch_list, days_prop)

    # Save to Excel
    excel_path = f'{file_name}.xlsx'
    df.to_excel(excel_path, index=False, sheet_name='Watch List')

    workbook = load_workbook(filename=excel_path)
    worksheet = workbook.active

    formatExcel(df, worksheet)

    workbook.save(filename=excel_path)


if __name__ == '__main__':
    # Initialize the watch list
    wl = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    wl = getData('old', wl, guards_list, guard_points)

    days = getDays(wl)

    wl = getWatchListData(wl, days)

    exportToExcel('watch_list', wl, days)
