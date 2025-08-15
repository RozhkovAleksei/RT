from time import sleep

from loguru import logger
from pyautogui import press

from related_funcs_and_variables import globals as gl
from related_funcs_and_variables.externals import sleep_long, sleep_short


@logger.catch(reraise=True)
def set_type_of_dispatch(mobj):

    gl.SetRailTariffWindowActiveForInput(4)

    if mobj.type_dispatch.lower() == "г":
        try:
            press("down")
            sleep(sleep_long)
            press("enter")
        except:
            print(set_type_of_dispatch.__name__, " проблема - групповая отправка")
            gl.ExitByError()

    if mobj.type_dispatch.lower() == "м":
        try:
            for i in range(0, 2):
                sleep(sleep_short)
                press("down")
            sleep(sleep_short)
            press("enter")
        except:
            print(set_type_of_dispatch.__name__, " проблема - маршрутная отправка")
            gl.ExitByError()

    if mobj.type_dispatch.lower() == "к":
        try:
            for i in range(0, 3):
                press("down")
                sleep(sleep_short)
            press("tab")
            sleep(sleep_short)

            for i in range(0, 2):
                press("down")
                sleep(sleep_short)
            sleep(sleep_short)
            press("space")
            sleep(sleep_short)
            press("tab")
            sleep(sleep_short)
            if mobj.is_container_train == "1":
                press("down")
                sleep(sleep_short)

            press("space")
            press("enter")
        except:
            print(set_type_of_dispatch.__name__, " проблема - контейнерная отправка")
            gl.ExitByError()

    sleep(sleep_short)
