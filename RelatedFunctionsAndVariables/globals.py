from pyautogui import keyDown, keyUp, press
from pygetwindow import getWindowsWithTitle
from time import sleep
import sys
from py_win_keyboard_layout import change_foreground_window_keyboard_layout
from win32api import GetSystemMetrics
import win32gui
import pyscreeze
from loguru import logger
from RelatedFunctionsAndVariables.externals import sleep_short, sleep_moment, sleep_long


# Функция для того, чтобы сделать активным окно программы RT
@logger.catch(reraise=True)
def SetRailTariffWindowActive():
    # Переключается раскладка на английскую независимо от текущей, нужно для ввода с клавиатуры
    change_foreground_window_keyboard_layout(0x04090409)

    sleep(sleep_moment)

    try:
        rail_tariff_window = getWindowsWithTitle('Новый расчёт - R-Тариф')[0]
        sleep(sleep_long)
        if rail_tariff_window.isActive is not True:
            rail_tariff_window.activate()
            sleep(sleep_long)
    except:
        print(SetRailTariffWindowActive.__name__, ' проблема - не найдено окно R-Тариф')
        sys.exit()

# Функция для того, чтобы сделать активным окно программы RT и запустить комбинацию горячих клавиш
@logger.catch(reraise=True)
def SetRailTariffWindowActiveForInput(hotkey_number):

    sleep(sleep_moment)

    try:
        SetRailTariffWindowActive()

        # Ввод горячих клавиш для открытия соответствующих окон для ввода параметров расчета
        keyDown('ctrl')
        sleep(sleep_moment)
        press(str(hotkey_number))
        sleep(sleep_moment)
        keyUp('ctrl')
        sleep(sleep_moment)
    except:
        print(SetRailTariffWindowActiveForInput.__name__, ' проблема - не найдено окно для ввода')
        sys.exit()

# Когда что-то пошло не так, то нужен выход с гарантией выхода, потому что зависает и теряет окно в непредсказуемых местах
@logger.catch(reraise=True)
def ExitByError():
    print(ExitByError.__name__)
    SetRailTariffWindowActive()
    sleep(sleep_long)
    press('esc')
    sleep(sleep_long)
    press('esc')
    sleep(sleep_long)
    press('esc')
    sleep(sleep_long)
    press('tab')
    sleep(sleep_long)
    press('esc')
    sleep(sleep_long)
    sys.exit()

# Блок для определения отдельных параметров, в зависимости от локального компьютера, на котором происходит проверка
# Big monitor resolution:
# 3840 x 1600
# Small monitor resolution:
# 1920 x 1080
# scr_width GetSystemMetrics(0)
# scr_height GetSystemMetrics(1)
@logger.catch(reraise=True)
def SetPathToImgByScreenRes():

    screen_res = [GetSystemMetrics(0), GetSystemMetrics(1)]
    if screen_res[0] != 1920:
        return "ImgData/HighRes/"
    else:
        return "ImgData/"

@logger.catch(reraise=True)
def SetDiskLabelByScreenRes():

    screen_res = [GetSystemMetrics(0), GetSystemMetrics(1)]
    if screen_res[0] != 1920:
        return "Y"
    else:
        return "Z"

@logger.catch(reraise=True)
def gng_extra_option_finder() -> str:

    # В зависимости от компьютера, на котором проверяется код - выбирается метка диска, где лежит файл excel.
    path_to_img_data = SetPathToImgByScreenRes()

    SetRailTariffWindowActive()

    gng_not_defined_content = None

    gng_defined_content = None

    sleep(sleep_short)

    gng_extra_option_window = win32gui.FindWindow(None, "Классификатор грузов ГНГ")

    gng_extra_option_window_coord = win32gui.GetWindowRect(gng_extra_option_window)

    if gng_extra_option_window is not None:
        try:
            SetRailTariffWindowActive()

            gng_not_defined_content = pyscreeze.locateOnScreen(path_to_img_data + "GNG_not_defined.png",
                                                               # grayscale=True,
                                                               confidence=0.98,
                                                               region=(
                                                                   gng_extra_option_window_coord[0],
                                                                   gng_extra_option_window_coord[1],
                                                                   gng_extra_option_window_coord[2] -
                                                                   gng_extra_option_window_coord[0],
                                                                   gng_extra_option_window_coord[3] -
                                                                   gng_extra_option_window_coord[1]),
                                                               # limit=1,
                                                               # minSearchTime=min_search_time
                                                                                                        )

        except Exception as gng_not_def_excp:
            # print("ГНГ окно с неопределенным кодом не найдено")
            print("gng_not_def_excp", gng_not_def_excp)

        try:
            SetRailTariffWindowActive()

            gng_defined_content = pyscreeze.locateOnScreen(path_to_img_data + "GNG_defined.png",
                                                               # grayscale=True,
                                                               confidence=0.98,
                                                               region=(
                                                                   gng_extra_option_window_coord[0],
                                                                   gng_extra_option_window_coord[1],
                                                                   gng_extra_option_window_coord[2] -
                                                                   gng_extra_option_window_coord[0],
                                                                   gng_extra_option_window_coord[3] -
                                                                   gng_extra_option_window_coord[1]),
                                                               # limit=1,
                                                               # minSearchTime=min_search_time
                                                                                                        )
        except Exception as gng_def_excp:
            # print("ГНГ окно с определенным кодом не найдено")
            print("gng_def_excp", gng_def_excp)

        # print("gng_not_defined_content =", gng_not_defined_content)
        # print("gng_defined_content =", gng_defined_content)

        if (gng_not_defined_content is not None) and (gng_defined_content is None):
            # print("return not_defined")
            return "gng_not_defined"
        if (gng_not_defined_content is None) and (gng_defined_content is not None):
            # print("return defined")
            return "gng_defined"
    else:
        print("Окно должно быть, но не найдено! Выход по ошибке.")
        SetRailTariffWindowActive()
        ExitByError()

