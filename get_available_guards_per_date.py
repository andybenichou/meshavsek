from collections import defaultdict

import pandas as pd
from openpyxl import load_workbook

from GuardsList import GuardsList
from consts import DAY_COLUMN_NAME, HOUR_COLUMN_NAME, \
    AVAILABLE_GUARDS_COLUMN_NAME, AVAILABLE_GUARDS_FILE_NAME
from export import parse_date, is_row_empty, format_excel


def format_to_excel_data_frame(available_guards_per_date):
    columns = [DAY_COLUMN_NAME, HOUR_COLUMN_NAME, AVAILABLE_GUARDS_COLUMN_NAME]
    data = list()

    for date in available_guards_per_date:
        time_for_excel = f'{date.hour:02d}:00'  # formatted for Excel
        row = [parse_date(date), time_for_excel]

        guards_str = ', '.join(
            [str(g) for g in available_guards_per_date[date]]) \
            if available_guards_per_date[date] else ' '

        row.append(guards_str)

        if not is_row_empty(row):
            data.append(row)

    return pd.DataFrame(data, columns=columns)


def export_to_excel(file_name, available_guards_per_date):
    df = format_to_excel_data_frame(available_guards_per_date)

    # Save to Excel
    excel_path = f'{file_name}.xlsx'
    df.to_excel(excel_path, index=False, sheet_name='Available')

    workbook = load_workbook(filename=excel_path)
    worksheet = workbook.active

    format_excel(df, worksheet)

    workbook.save(filename=excel_path)


def get_available_guards_per_date(wl, guards_list, file_name, backward_delay=0,
                                  forward_delay=0):
    available_guards_per_date = defaultdict(GuardsList)
    for index, date in enumerate(wl):
        if index < backward_delay or index >= len(wl) - forward_delay:
            continue

        for guard in guards_list:
            if guard.is_available(wl, date, spot=None,
                                  delays_prop=list(range(-backward_delay,
                                                         forward_delay + 1, 3)),
                                  not_missing_delay=forward_delay) \
                    and guard not in available_guards_per_date[date]:
                available_guards_per_date[date].append(guard)

    export_to_excel(file_name, available_guards_per_date)

    return available_guards_per_date
