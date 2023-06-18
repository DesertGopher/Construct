import datetime
import os
from pathlib import Path

import openpyxl
import pandas as pd
from openpyxl.styles import Font


def set_width(filepath):
    wb = openpyxl.load_workbook(filename=filepath)
    ws = wb.active

    font_size = 14
    cols_dict = {}

    for row in ws.rows:
        for cell in row:
            letter = cell.column_letter
            if cell.value:
                cell.font = Font(name='Calibri', size=font_size)
                len_cell = len(str(cell.value))

                len_cell_dict = 0
                if letter in cols_dict:
                    len_cell_dict = cols_dict[letter]

                if len_cell > len_cell_dict:
                    cols_dict[letter] = len_cell
                    new_width_col = len_cell * font_size ** (font_size * 0.01)
                    ws.column_dimensions[cell.column_letter].width = new_width_col

    wb.save(filepath)
    wb.close()


def generate_report(orders):
    users_list = []
    orders_list = []
    costs_list = []
    dates_list = []
    for item in orders:
        users_list.append(item.client_id)
        orders_list.append(item)
        costs_list.append(item.total_cost)
        date = item.date_created.strftime("%Y-%B-%A")
        dates_list.append(str(date))

    df = pd.DataFrame({'Клиент': users_list,
                       'Заказ': orders_list,
                       'Дата': dates_list,
                       'Стоимость, руб.': costs_list})
    df.at[len(orders) + 1, 'Стоимость, руб.'] = df['Стоимость, руб.'].sum()
    df.at[len(orders) + 1, 'Дата'] = "Итого"

    pd.set_option('max_colwidth', None)

    directory = Path(__file__).resolve().parent
    hour = "{:02d}".format(datetime.datetime.now().hour)
    minute = "{:02d}".format(datetime.datetime.now().minute)
    second = "{:02d}".format(datetime.datetime.now().second)
    hms_n = "{}-{}-{}".format(hour, minute, second)
    filename = f"Rev_report_{hms_n}.xlsx"
    output = os.path.abspath(directory / "reports" / filename)

    df.to_excel(output, sheet_name="revenue", index=False)
    set_width(output)
