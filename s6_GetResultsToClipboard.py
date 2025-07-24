import keyboard
from time import sleep
import py_win_keyboard_layout
import pandas as pd
import globals as gl
from externals import sleep_short
from loguru import logger

@logger.catch(reraise=True)
def get_results_to_clipboard_and_fill_object(mobj):

    # Переключение раскладки на английскую независимо от текущей, нужно для ввода с клавиатуры
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)

    # Переключение на окно с RT
    gl.SetRailTariffWindowActive()

    sleep(sleep_short)

    # Горячие клавиши окна RT - копирование таблицы результатов расчётов
    keyboard.press("ctrl")
    keyboard.press("t")
    keyboard.release("t")
    keyboard.release("ctrl")

    sleep(sleep_short)

    # Считывание и очищение буфера обмена - вставка в новый dataframe
    df_tmp = pd.read_clipboard(dtype=str)
    sleep(sleep_short)

    df_tmp.rename(columns={" ": "Напр."}, inplace=True)
    sleep(sleep_short)

    # print(df_tmp)

    # Парсинг dataframe для заполнения полей атрибутов класса результатами расчёта i-й корреспонденции
    for index, row in df_tmp.iterrows():
        if row["Страна"] == "Россия" and row["Напр."] == '→':
            mobj.mainland_payment_by_loaded_carriage = row['Пров. пл.']
            mobj.mainland_currency_of_result = row["Валюта"]

        if row["Страна"] == "Россия" and row["Напр."] == '←':
            mobj.mainland_payment_by_empty_carriage = row['Пров. пл.']
            mobj.mainland_payment_distance = row['Расст., км']

        if row["Страна"] == "Крым" and row["Напр."] == '→':
            mobj.crimea_payment_by_loaded_carriage = row['Пров. пл.']
            mobj.crimea_currency_of_result = row["Валюта"]

        if row["Страна"] == "Крым" and row["Напр."] == '←':
            mobj.crimea_payment_by_empty_carriage = row['Пров. пл.']
            mobj.crimea_payment_distance = row['Расст., км']

        if row["Страна"] == "Сахалин" and row["Напр."] == '→':
            mobj.sakhalin_payment_by_loaded_carriage = row['Пров. пл.']
            mobj.sakhalin_currency_of_result = row["Валюта"]

        if row["Страна"] == "Сахалин" and row["Напр."] == '←':
            mobj.sakhalin_payment_by_empty_carriage = row['Пров. пл.']
            mobj.sakhalin_payment_distance = row['Расст., км']

        if row["Страна"] == "Казахстан" and row["Напр."] == '→':
            mobj.kazakhstan_payment_by_loaded_carriage = row['Пров. пл.']
            mobj.kazakhstan_currency_of_result = row["Валюта"]

        if row["Страна"] == "Казахстан" and row["Напр."] == '←':
            mobj.kazakhstan_payment_by_empty_carriage = row['Пров. пл.']
            mobj.kazakhstan_payment_distance = row['Расст., км']

        if row["Страна"] == "Литва" and row["Напр."] == '→':
            mobj.litva_payment_by_loaded_carriage = row['Пров. пл.']
            mobj.litva_currency_of_result = row["Валюта"]

        if row["Страна"] == "Литва" and row["Напр."] == '←':
            mobj.litva_payment_by_empty_carriage = row['Пров. пл.']
            mobj.litva_payment_distance = row['Расст., км']

        if row["Страна"] == "Беларусь" and row["Напр."] == '→':
            mobj.belarus_payment_by_loaded_carriage = row['Пров. пл.']
            mobj.belarus_currency_of_result = row["Валюта"]

        if row["Страна"] == "Беларусь" and row["Напр."] == '←':
            mobj.belarus_payment_by_empty_carriage = row['Пров. пл.']
            mobj.belarus_payment_distance = row['Расст., км']

        if row["Страна"] == "ЖДН" and row["Напр."] == '→':
            mobj.zhdn_payment_by_loaded_carriage = row['Пров. пл.']
            mobj.zhdn_currency_of_result = row["Валюта"]

        if row["Страна"] == "ЖДН" and row["Напр."] == '←':
            mobj.zhdn_payment_by_empty_carriage = row['Пров. пл.']
            mobj.zhdn_payment_distance = row['Расст., км']

    sleep(sleep_short)

