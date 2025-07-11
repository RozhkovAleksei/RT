import pandas as pd
import pyautogui as pag
from time import sleep
import globals
import py_win_keyboard_layout


def GetDetailsFromRTarif(row_num, det_folder):

    globals.SetRailTariffWindowActive()

    sleep(0.5)

    # Здесь идёт перешагивание по активным областям окна интерфейса программы

    # Встаём в поле с вводом даты (гарантированная начальная точка навигации в окне)
    # Из-за того, что иногда система не отпускает зажатый Ctrl - сделано специально - нажатие и отпуск.
    pag.keyDown('ctrl')
    pag.keyDown('d')
    pag.keyUp('d')
    pag.keyUp('ctrl')

    sleep(0.5)

    pag.press('tab')
    sleep(0.5)
    pag.press('tab')

    sleep(0.5)

    pag.keyDown('ctrl')
    pag.keyDown('tab')
    pag.keyUp('tab')
    pag.keyUp('ctrl')

    sleep(0.5)
    pag.press('tab')
    sleep(0.3)
    pag.press('up')
    sleep(0.3)
    pag.press('up')
    sleep(0.3)
    pag.press('right')
    sleep(0.3)
    pag.press('right')
    sleep(0.3)
    pag.press('right')
    sleep(0.5)
    pag.press('down')
    sleep(0.5)
    pag.press('enter')


    # Переключение раскладки на английскую независимо от текущей, нужно для ввода с клавиатуры
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)
    # pag.hotkey('ctrl', 'y')
    pag.keyDown('ctrl')
    pag.keyDown('y')
    pag.keyUp('y')
    pag.keyUp('ctrl')

    sleep(0.5)

    # Считывается во временный датафрейм из буфера обмена информация
    df_tmp_1 = pd.read_clipboard()
    sleep(0.1)

    globals.SetRailTariffWindowActive()

    sleep(0.1)
    pag.press('down')
    sleep(0.3)
    pag.press('enter')
    sleep(0.3)

    # Переключение раскладки на английскую независимо от текущей, нужно для ввода с клавиатуры
    py_win_keyboard_layout.change_foreground_window_keyboard_layout(0x04090409)

    pag.keyDown('ctrl')
    pag.keyDown('y')
    pag.keyUp('y')
    pag.keyUp('ctrl')

    sleep(0.2)
    df_tmp_2 = pd.read_clipboard()
    sleep(0.1)

    with pd.ExcelWriter(str(str(det_folder) + str(row_num) + '.xlsx'), mode='w', engine='openpyxl') as writer:
        sleep(0.3)
        df_tmp_1.to_excel(writer, sheet_name="loaded")
        sleep(0.3)
        df_tmp_2.to_excel(writer, sheet_name="empty")

