from time import sleep

import pandas as pd
import py_win_keyboard_layout
import pyautogui as pag
from loguru import logger

from related_funcs_and_variables import globals as gl
from related_funcs_and_variables.externals import (
    sleep_long,
    sleep_moment,
    sleep_short,
    sleep_tic,
)

pag.FAILSAFE = False

@logger.catch(reraise=True)
# async def export_details_to_new_excels(det_folder, my_obj):
def export_details_to_new_excels(det_folder, my_obj):
    """Функция выгружает детализированные данные в отдельные файлы"""

    gl.SetRailTariffWindowActive()

    sleep(sleep_long)

    # Здесь идёт перешагивание по активным областям окна интерфейса программы

    # Встаём в поле с вводом даты (гарантированная начальная точка навигации в окне)
    # Из-за того, что иногда система не отпускает зажатый Ctrl - сделано специально - нажатие и отпуск.
    pag.keyDown("ctrl")
    pag.keyDown("d")
    pag.keyUp("d")
    pag.keyUp("ctrl")

    sleep(sleep_long)

    pag.press("tab")
    sleep(sleep_long)
    pag.press("tab")

    sleep(sleep_long)

    pag.keyDown("ctrl")
    pag.keyDown("tab")
    pag.keyUp("tab")
    pag.keyUp("ctrl")

    sleep(sleep_long)
    pag.press("tab")
    sleep(sleep_short)
    pag.press("up")
    sleep(sleep_short)
    pag.press("up")
    sleep(sleep_short)
    pag.press("right")
    # sleep(sleep_short)
    # pag.press("right")
    # sleep(sleep_short)
    # pag.press("right")
    sleep(sleep_long)
    pag.press("down")
    sleep(sleep_long)
    pag.press("enter")

    # Переключение раскладки на английскую независимо от текущей, нужно для ввода с клавиатуры
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)

    pag.keyDown("ctrl")
    pag.keyDown("y")
    pag.keyUp("y")
    pag.keyUp("ctrl")

    sleep(sleep_long)

    # Считывается во временный датафрейм из буфера обмена информация
    df_tmp_1 = pd.read_clipboard()
    sleep(sleep_tic)

    gl.SetRailTariffWindowActive()

    sleep(sleep_tic)
    pag.press("down")
    sleep(sleep_short)
    pag.press("enter")
    sleep(sleep_short)

    # Переключение раскладки на английскую независимо от текущей, нужно для ввода с клавиатуры
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)

    pag.keyDown("ctrl")
    pag.keyDown("y")
    pag.keyUp("y")
    pag.keyUp("ctrl")

    sleep(sleep_moment)
    df_tmp_2 = pd.read_clipboard()
    sleep(sleep_tic)

    with pd.ExcelWriter(
        str(
            det_folder
            + my_obj.station_otpr_name
            + "-"
            + my_obj.station_nazn_name
            + "-"
            + my_obj.etsng_cargo
            + "-"
            + my_obj.type_dispatch
            + "-"
            + my_obj.date_calculation
            + ".xlsx"
        ),
        mode="w",
        engine="openpyxl",
    ) as writer:
        sleep(sleep_short)
        df_tmp_1.to_excel(writer, sheet_name="loaded")
        sleep(sleep_short)
        df_tmp_2.to_excel(writer, sheet_name="empty")
