import csv
import os
import random
import pandas as pd

from collections import defaultdict
from datetime import datetime
from itertools import cycle

from openpyxl import load_workbook
from openpyxl.styles import Alignment
from getData import get_data


RANDOMNESS_LEVEL = 5

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
guards_list = ['יואל', 'ליאור', 'אבנר', 'משה', 'יונג', 'דורון',
               'רוני', 'אסרף', 'שגיא', 'אנדי', 'דוד', 'אנזו', 'לישי',
               'דימנטמן', 'איתי כהן', 'דעאל', 'אגומס', 'מטמוני', 'ניסנוב',
               'אור', 'עמיחי', 'לוטם', 'שרעבי', 'לואיס', 'דובר', 'שראל',
               'אלכסיי', 'דבוש', 'דותן', 'אסף', 'דמיטרי', 'רווה', 'כלפה',
               'לומיאנסקי', 'נפמן', 'סדון', 'סיני', 'שמעון', 'פיאצה',
               'קריספין', 'ארד', 'שבצוב', 'משה החופל']

# List of duos
duos = [('אנדי', 'דוד'), ('דימנטמן', 'מטמוני')]

# List of missing guards each day
# For now the missing guards are only from 12 to 14 the next day.
# TODO: Make a missing constraint by hours
missings = {
    'Sunday': [],
    'Monday': [],
    'Tuesday': [],
    'Wednesday': [],
    'Thursday': [],
    'Friday': [],
    'Saturday': []
}

# Define the days
week_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
             'Thursday', 'Friday', 'Saturday']


class CurrentGuard:
    __current_guard = None

    def get_current_guard(self):
        return self.__current_guard

    def set_current_guard(self, new_guard):
        self.__current_guard = new_guard


current_guard = CurrentGuard()


def get_last_guard_time():
    pass


def get_prec_day(day_prop, days_prop):
    day_i = days_prop.index(day_prop)
    prec_day = None

    if day_i > 0:
        prec_day = days_prop[day_i - 1]

    return prec_day


def is_guard_missing(guard, day_prop, time_prop, days_prop):
    prec_day = get_prec_day(day_prop, days_prop)
    hour = int(time_prop[:2])

    # Check if in missings guards
    if (guard in missings[day_prop] and hour >= 12) or \
            (prec_day and
             guard in missings[prec_day] and
             hour <= 14):
        return True

    return False


# Helper function to check if a guard is available
def is_guard_available(watch_list, guard, day_prop, time_prop, days_prop, test=False):
    if is_guard_missing(guard, day_prop, time_prop, days_prop):
        return False

    hour = int(time_prop[:2])

    for rest_delay in [0, 3, 6]:
        updated_hour = hour - rest_delay
        updated_day = day_prop

        if updated_hour < 0:
            updated_day = get_prec_day(day_prop, days_prop)
            updated_hour += 24

        if not updated_day:
            break

        # Check if the guard already in another point
        for p in guard_points:
            for t in guard_points[p]:
                beginning_str, g_end_str = t.split('-')
                beginning, g_end = map(int, [beginning_str[:2], g_end_str[:2]])

                if g_end < beginning:
                    g_end += 24

                    if beginning <= updated_hour + 24 < g_end:
                        updated_hour += 24

                slot_d = updated_day

                if beginning <= updated_hour < g_end:
                    if updated_hour >= 24:
                        slot_d = get_prec_day(updated_day, days_prop)

                        if not slot_d:
                            break

                    if guard in watch_list[slot_d][beginning_str][p]:
                        return False

    return True


# Align guards cycle to the next available guard
def align_guards_cycle(watch_list, guard_cycle_prop,
                       day_prop, time_prop, days_prop):
    guard = current_guard.get_current_guard()

    if not guard:
        guard = next(guard_cycle_prop)
        current_guard.set_current_guard(guard)

    while not is_guard_available(watch_list, guard, day_prop,
                                 time_prop, days_prop, test=True):
        guard = next(guard_cycle_prop)
        current_guard.set_current_guard(guard)

    return guard


# Helper function to get the next available guard
def get_next_available_guard(watch_list, guard_cycle_prop, day_prop,
                             time_prop, days_prop, guards=None,
                             no_duo=False):
    current_guard = align_guards_cycle(watch_list, guard_cycle_prop,
                                       day_prop, time_prop, days_prop)
    index = guards_list.index(current_guard)
    buff_cycle = cycle(guards_list[index:] + guards_list[:index])

    while True:
        random_guards = list()
        while len(random_guards) != RANDOMNESS_LEVEL:
            guard = next(buff_cycle)

            if is_guard_available(watch_list, guard, day_prop,
                                  time_prop, days_prop) \
                    and guard not in guards:
                random_guards.append(guard)

        random.shuffle(random_guards)

        for guard in random_guards:
            duo = next((duo for duo in duos if guard in duo), None)
            if duo:
                partner = duo[0] if duo[1] == guard else duo[1]

                if is_guard_missing(partner, day_prop, time_prop, days_prop):
                    return guard, None

                if no_duo:
                    continue

                elif is_guard_available(watch_list, partner, day_prop,
                                        time_prop, days_prop):
                    return guard, partner

            else:
                return guard, None


def get_today_day_of_week():
    # Get the current date
    today = datetime.today()

    # Get the name of the day of the week
    day_name = today.strftime("%A")

    return day_name


def get_days(watch_list):
    user_input = input("How many days do you need to schedule? ")

    while True:
        if user_input.isdigit():
            days_num = int(user_input)
            break
        else:
            user_input = input("Please enter a valid integer. ")

    days_list = list(watch_list.keys()) if watch_list.keys() else get_today_day_of_week()
    days_cycle = cycle(week_days)

    day = next(days_cycle)
    while days_list[-1] != day:
        day = next(days_cycle)

    for _ in range(days_num):
        day = next(days_cycle)

        if day in days_list:
            break

        days_list.append(day)

    return days_list


def get_already_filled_guard_slot(watch_list, day, time, hour, point,
                                  days_prop):
    guards = watch_list[day][time][point] if watch_list[day][time][point] else list()
    fill_guard_point = False

    # Point already filled
    if len(guards) == 2:
        return guards, fill_guard_point

    for slot in guard_points[point]:
        # Fill the actual hour with the slot guards if there are
        # already in one of the slot hour
        start_str, end_str = slot.split('-')
        start, end = int(start_str[:2]), int(end_str[:2])

        if end < start:
            end += 24

            if start <= hour + 24 < end:
                hour += 24

        if start <= hour < end:
            fill_guard_point = True

        if start < hour < end:
            slot_day = day
            if hour == 24:
                day_index = days_prop.index(day)

                if day_index > 0:
                    slot_day = days_prop[day_index - 1]

            guards = watch_list[slot_day][f'{((hour - 1) % 24):02d}00'][point]

    return guards, fill_guard_point


def get_guards(watch_list, guard_cycle, day, time, hour, point,
               days_prop):
    guards, fill_guard_point = \
        get_already_filled_guard_slot(watch_list,
                                      day, time, hour, point,
                                      days_prop)

    if len(guards) == 2:
        return guards

    if fill_guard_point:
        guard1, guard2 = get_next_available_guard(watch_list,
                                                  guard_cycle,
                                                  day,
                                                  time,
                                                  days_prop,
                                                  guards=guards)

        for g in [guard1, guard2]:
            if len(guards) != 2 and g:
                guards.append(g)

        if len(guards) == 1:
            guard2 = get_next_available_guard(watch_list,
                                              guard_cycle,
                                              day,
                                              time,
                                              days_prop,
                                              guards=guards,
                                              no_duo=True)[0]
            guards.append(guard2)
        guards.sort()

    return guards


def get_watch_list_data(watch_list, days_prop):
    # Assign guards to each slot
    guard_cycle = cycle(guards_list)
    for day in days_prop:
        for time in sorted(set([f'{hour:02d}00' for hour in range(24)])):
            hour = int(time[:2])

            # Remove unnecessary start and end of planning
            if (days_prop.index(day) == 0 and hour < 2) or \
                    (days_prop.index(day) == len(days_prop) - 1
                     and hour >= 20):
                continue

            for point in guard_points:
                guards = get_guards(watch_list, guard_cycle,
                                    day, time, hour, point, days_prop)

                if len(guards) == 2 and not watch_list[day][time][point]:
                    watch_list[day][time][point].extend(guards)

    return watch_list


def export_to_CSV(watch_list, days_prop):
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


def get_excel_data_frame(watch_list, days_prop):
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


def merge_excel_cells(df, worksheet):
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


def adjust_columns_and_rows(worksheet):
    # Adjust the column width according to content, wrap text, and center align
    # text
    for col in worksheet.columns:
        max_length = 0
        column = [cell for cell in col]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))

                # Set wrap text and center alignment
                cell.alignment = Alignment(wrap_text=True, horizontal='center',
                                           vertical='center')
            except:
                pass
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width


def format_excel(df, worksheet):
    merge_excel_cells(df, worksheet)
    adjust_columns_and_rows(worksheet)


def export_to_excel(file_name, watch_list, days_prop):
    df = get_excel_data_frame(watch_list, days_prop)

    # Save to Excel
    excel_path = f'{file_name}.xlsx'
    df.to_excel(excel_path, index=False, sheet_name='Watch List')

    workbook = load_workbook(filename=excel_path)
    worksheet = workbook.active

    format_excel(df, worksheet)

    workbook.save(filename=excel_path)


if __name__ == '__main__':
    # Initialize the watch list
    wl = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    old_file_name = 'old'
    src_dir = os.path.dirname(os.path.abspath(__file__))
    old_dir = os.path.join(src_dir, f'{old_file_name}.xlsx')

    if os.path.exists(old_dir):
        wl = get_data(old_file_name, wl, guards_list, guard_points)

    days = get_days(wl)

    for d in days:
        if d not in wl.keys():
            wl[d] = defaultdict(lambda: defaultdict(list))

    wl = get_watch_list_data(wl, days)

    export_to_excel('watch_list', wl, days)

    print('Shivsakta!')
