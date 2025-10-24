from time import sleep

import pyautogui as pag
from loguru import logger

from related_funcs_and_variables import globals as gl
from related_funcs_and_variables.externals import sleep_long, sleep_short

pag.FAILSAFE = False

# Блок установки станции возврата вагона для расчета тарифа в порожнем рейсе
@logger.catch(reraise=True)
def set_car_return_option():

    gl.SetRailTariffWindowActiveForInput(8)
    sleep(sleep_short)
    pag.press("down")
    sleep(sleep_short)
    pag.press("space")
    sleep(sleep_short)
    pag.press("enter")
    sleep(sleep_long)
