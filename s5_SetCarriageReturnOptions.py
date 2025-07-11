from time import sleep
import pyautogui as pag
import globals

# Блок установки станции возврата вагона для расчета тарифа в порожнем рейса
def SetReturn(mobj):

    globals.SetRailTariffWindowActiveForInput(8)
    sleep(mobj.global_sleep_short)
    pag.press('down')
    sleep(mobj.global_sleep_short)
    pag.press('space')
    sleep(mobj.global_sleep_short)
    pag.press('enter')
    sleep(mobj.global_sleep_long)

