import csv
from datetime import datetime

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, Border, Side, Alignment
from openpyxl.utils.exceptions import IllegalCharacterError


def export_to_CSV(watch_list, guard_spots):
    with open('watch_list.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        header = ['יום', 'שעה'] + list(guard_spots.keys())
        csvwriter.writerow(header)
        for date in watch_list:
            row = [date]

            for spot in guard_spots.keys():
                guards_str = '\n'.join(watch_list[date][spot]) \
                    if watch_list[date][spot] else ' '
                row.append(guards_str)
            csvwriter.writerow(row)


def is_row_entry(row):
    is_row_empty = True
    for guards_str in row[2:]:
        if len(guards_str) > 1:
            is_row_empty = False

    return is_row_empty


def parse_date(date: datetime):
    return date.date()


def get_excel_data_frame(watch_list, guard_spots, duty_room_per_day, kitot_konenout):
    columns = ['יום', 'שעה'] + list(guard_spots.keys()) + ['כתת כוננות']
    data = list()

    for date in watch_list:
        time_for_excel = f'{date.hour:02d}:00'  # formatted for Excel
        row = [parse_date(date), time_for_excel]

        for spot in guard_spots.keys():
            guards_str = '\n'.join(
                [str(g) for g in watch_list[date][spot]]) \
                if watch_list[date][spot] else ''

            midgnight_date = date.replace(hour=0)
            if spot == 'פטרול' and not guards_str \
                    and midgnight_date in duty_room_per_day \
                    and not is_row_entry(row):
                row.append(f'{duty_room_per_day[midgnight_date]} תורני רס"פ - חדר')

            elif guards_str:
                row.append(guards_str)

        if not is_row_entry(row) \
                and date in kitot_konenout  \
                and kitot_konenout[date] is not None:
            row.append(f'{kitot_konenout[date]} חדר')

        if not is_row_entry(row):
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


def is_column_empty(worksheet, column_index):
    # Iterate through each cell in the column
    for row in worksheet.iter_rows(min_col=column_index, max_col=column_index):
        cell = row[0]  # Since we're looking at one column, there's only one cell per row tuple
        if cell.value is not None:
            return False  # Found a cell with data, so the column is not empty
    return True  # All cells in the column are empty


def adjust_columns_and_rows(worksheet):
    # Define font, alignment, and border styles
    bold_font = Font(bold=True, size=12)
    center_aligned_text = Alignment(horizontal='center', vertical='center',
                                    text_rotation=0, readingOrder=1)
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for index, col in enumerate(worksheet.columns, start=1):
        if is_column_empty(worksheet, index):
            continue

        max_length = 0
        column = [cell for cell in col]
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
                # Apply styles
                cell.font = bold_font
                cell.alignment = center_aligned_text
                cell.border = thin_border  # Apply border to each cell
            except IllegalCharacterError:
                # Handle specific openpyxl IllegalCharacterError
                pass
            except Exception as e:
                # You can log the exception if needed
                print(f"An error occurred: {e}")
        adjusted_width = (max_length + 2)
        worksheet.column_dimensions[column[0].column_letter].width = adjusted_width


def format_excel(df, worksheet):
    merge_excel_cells(df, worksheet)
    adjust_columns_and_rows(worksheet)


def export_to_excel(file_name, watch_list, guard_spots, duty_room_per_day, kitot_konenout):
    df = get_excel_data_frame(watch_list, guard_spots, duty_room_per_day, kitot_konenout)

    # Save to Excel
    excel_path = f'{file_name}.xlsx'
    df.to_excel(excel_path, index=False, sheet_name='שבצ״כ')

    workbook = load_workbook(filename=excel_path)
    worksheet = workbook.active

    format_excel(df, worksheet)

    workbook.save(filename=excel_path)
