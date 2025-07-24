from time import sleep
import pyautogui as pag
import globals as gl
from externals import sleep_short, sleep_long
from loguru import logger


# Блок установки станции возврата вагона для расчета тарифа в порожнем рейсе
@logger.catch(reraise=True)
def set_car_return_option():

    gl.SetRailTariffWindowActiveForInput(8)
    sleep(sleep_short)
    pag.press('down')
    sleep(sleep_short)
    pag.press('space')
    sleep(sleep_short)
    pag.press('enter')
    sleep(sleep_long)

