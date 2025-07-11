from pyautogui import hotkey, press, keyDown, keyUp
from keyboard import write
from time import sleep
from py_win_keyboard_layout import change_foreground_window_keyboard_layout
import globals

def SetNewCalculation(mobj):

    # Переключается раскладка на английскую независимо от текущей, нужно для ввода с клавиатуры
    change_foreground_window_keyboard_layout(0x04090409)

    sleep(0.3)

    globals.SetRailTariffWindowActive()
    press("esc")
    sleep(mobj.global_sleep_short)
    press("esc")
    sleep(mobj.global_sleep_short)
    press("esc")
    sleep(mobj.global_sleep_short)

    keyDown('ctrl')
    keyDown('n')
    keyUp('n')
    keyUp('ctrl')

    sleep(mobj.global_sleep_long)

    # Установление курсора для установки даты для расчёта
    keyDown('ctrl')
    keyDown('d')
    keyUp('d')
    keyUp('ctrl')
    # hotkey('ctrl', 'd')
    sleep(mobj.global_sleep_moment)
    write(str(mobj.calc_day), delay=0.01)
    sleep(mobj.global_sleep_moment)
    write(str(mobj.calc_month), delay=0.01)
    sleep(mobj.global_sleep_moment)
    write(str(mobj.calc_year), delay=0.01)
    sleep(mobj.global_sleep_moment)
    press('enter')
    sleep(mobj.global_sleep_moment)

