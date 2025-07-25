from pyautogui import press, keyDown, keyUp
from keyboard import write
from time import sleep
from py_win_keyboard_layout import change_foreground_window_keyboard_layout
from loguru import logger
import globals as gl
from externals import sleep_moment, sleep_long, sleep_short

@logger.catch(reraise=True)
def set_new_calculation(mobj):

    # Переключается раскладка на английскую независимо от текущей, нужно для ввода с клавиатуры
    change_foreground_window_keyboard_layout(0x04090409)

    sleep(sleep_short)

    gl.SetRailTariffWindowActive()
    sleep(sleep_short)

    # Команда для выполнения нового расчета в программе RT
    keyDown('ctrl')
    keyDown('n')
    keyUp('n')
    keyUp('ctrl')

    sleep(sleep_long)

    # Установление курсора для установки даты для расчёта
    keyDown('ctrl')
    keyDown('d')
    keyUp('d')
    keyUp('ctrl')

    sleep(sleep_moment)
    # Если вставлять значения - не воспринимает или работает криво, поэтому нужно "вписывать", для этого тип данных str
    write(mobj.day_for_tariff, delay=0.01)
    sleep(sleep_moment)
    write(mobj.month_for_tariff, delay=0.01)
    sleep(sleep_moment)
    write(mobj.year_for_tariff, delay=0.01)
    sleep(sleep_moment)
    press('enter')
    sleep(sleep_moment)

