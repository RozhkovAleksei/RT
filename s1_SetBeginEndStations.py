import pyautogui as pag
from time import sleep
import win32gui
import globals

def SetBeginEndStation(begin_station_ESR_code, end_station_ESR_code, mobj):

    # Вызов функции, делающей активным окно с программой RT и передающей для комбинации из горячих клавиш
    # Номер вызываемого окна в качестве аргумента функции (Ctrl+1,2 и т.д.)
    globals.SetRailTariffWindowActiveForInput(1)

    sleep(mobj.global_sleep_short)

    if begin_station_ESR_code == '#Н/Д':
        globals.ExitByError()
    else:
        sleep(mobj.global_sleep_long)
        pag.typewrite(str(begin_station_ESR_code), interval=0.05)
        sleep(mobj.global_sleep_long)
        pag.press('enter')
        sleep(mobj.global_sleep_short)
        wnd = win32gui.FindWindow(None, "station_otpr_name")
        if wnd != 0:
            mobj.is_ESR_correct = 0
            print("Проблема со станцией отправления")
            globals.ExitByError()

    sleep(mobj.global_sleep_short)

    globals.SetRailTariffWindowActiveForInput(2)

    sleep(mobj.global_sleep_short)

    # Вставляется код станции НАЗНАЧЕНИЯ, чтобы по фильтру ниже в окне появилось её название
    if end_station_ESR_code == '#Н/Д':
        globals.ExitByError()
    else:
        sleep(mobj.global_sleep_long)
        pag.typewrite(str(end_station_ESR_code), interval=0.05)
        sleep(mobj.global_sleep_long)
        pag.press('enter')
        sleep(mobj.global_sleep_short)
        wnd = win32gui.FindWindow(None, "station_nazn_name")
        if wnd != 0:
            mobj.is_ESR_correct = 0
            print("Проблема со станцией назначения")
            globals.ExitByError()

    sleep(mobj.global_sleep_short)

