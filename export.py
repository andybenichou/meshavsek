import csv

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment

from consts import FIRST_HOUR_FIRST_DAY, LAST_HOUR_LAST_DAY


def export_to_CSV(watch_list, days, guard_spots):
    with open('watch_list.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ['יום', 'שעה'] + list(guard_spots.keys())
        csvwriter.writerow(header)
        for day in days:
            for hour in range(24):
                time = f'{hour:02d}00'
                row = [day, time]

                for spot in guard_spots.keys():
                    guards_str = '\n'.join(watch_list[day][hour][spot]) \
                        if watch_list[day][hour][spot] else ' '
                    row.append(guards_str)
                csvwriter.writerow(row)


def get_excel_data_frame(watch_list, days, guard_spots, duty_room_per_day, kitot_konenout):
    columns = ['יום', 'שעה'] + list(guard_spots.keys()) + ['כתת כוננות']
    data = list()

    for day in days:
        for hour in range(24):
            if (days.index(day) == 0 and hour < FIRST_HOUR_FIRST_DAY) or \
                    (days.index(day) == len(days) - 1 and hour >= LAST_HOUR_LAST_DAY):
                continue

            time_for_excel = f'{hour:02d}:00'  # formatted for Excel
            row = [day, time_for_excel]

            for spot in guard_spots.keys():
                guards_str = '\n'.join(
                    [g.name for g in watch_list[day][hour][spot]]) \
                    if watch_list[day][hour][spot] else ''

                if spot == 'פטרול' and not guards_str \
                        and day in duty_room_per_day:
                    row.append(f'{duty_room_per_day[day]} תורני רס"פ - חדר')

                elif guards_str:
                    row.append(guards_str)

            is_row_empty = True
            for guards_str in row[2:]:
                if len(guards_str) > 1:
                    is_row_empty = False

            if not is_row_empty \
                    and day in kitot_konenout \
                    and hour in kitot_konenout[day] \
                    and kitot_konenout[day][hour]:
                row.append(f'{kitot_konenout[day][hour]} חדר')

            if not is_row_empty:
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
        worksheet.column_dimensions[
            column[0].column_letter].width = adjusted_width


def format_excel(df, worksheet):
    merge_excel_cells(df, worksheet)
    adjust_columns_and_rows(worksheet)


def export_to_excel(file_name, watch_list, days, guard_spots, duty_room_per_day, kitot_konenout):
    df = get_excel_data_frame(watch_list, days, guard_spots, duty_room_per_day, kitot_konenout)

    # Save to Excel
    excel_path = f'{file_name}.xlsx'
    df.to_excel(excel_path, index=False, sheet_name='שבצ״כ')

    workbook = load_workbook(filename=excel_path)
    worksheet = workbook.active

    format_excel(df, worksheet)

    workbook.save(filename=excel_path)
