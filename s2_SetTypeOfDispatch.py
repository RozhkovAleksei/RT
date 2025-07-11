from pyautogui import press
from time import sleep
import globals


def SetTypeOfDispatch(type_of_dispatch, mobj):

    globals.SetRailTariffWindowActiveForInput(4)

    if type_of_dispatch.lower() == 'г':
        try:
            press('down')
            sleep(0.5)
            press('enter')
        except:
            print(SetTypeOfDispatch.__name__, " проблема - групповая отправка")
            globals.ExitByError()

    if type_of_dispatch.lower() == 'м':
        try:
            for i in range(0, 2):
                sleep(mobj.global_sleep_short)
                press('down')
            sleep(mobj.global_sleep_short)
            press('enter')
        except:
            print(SetTypeOfDispatch.__name__, " проблема - маршрутная отправка")
            globals.ExitByError()

    if type_of_dispatch.lower() == 'к':
        try:
            for i in range(0, 3):
                press('down')
                sleep(mobj.global_sleep_short)
            press('tab')
            sleep(mobj.global_sleep_short)

            for i in range(0, 2):
                press('down')
                sleep(mobj.global_sleep_short)
            sleep(mobj.global_sleep_short)
            press('space')
            sleep(mobj.global_sleep_short)
            press('tab')
            sleep(mobj.global_sleep_short)
            if mobj.is_full_train_containers == 1:
                press('down')
                sleep(mobj.global_sleep_short)

            press('space')
            press('enter')
        except:
            print(SetTypeOfDispatch.__name__, " проблема - контейнерная отправка")
            globals.ExitByError()

    sleep(mobj.global_sleep_short)

