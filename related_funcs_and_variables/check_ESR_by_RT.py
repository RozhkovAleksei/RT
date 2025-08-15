from time import sleep

from keyboard import write
from loguru import logger
from pandas import concat
from py_win_keyboard_layout import change_foreground_window_keyboard_layout
from pyautogui import hotkey, keyDown, keyUp, press, typewrite
from tqdm import tqdm
from win32gui import FindWindow

from related_funcs_and_variables.externals import sleep_long, sleep_moment, sleep_tic
from related_funcs_and_variables.globals import (
    SetRailTariffWindowActive,
    SetRailTariffWindowActiveForInput,
)

# Блок для проверки кода станции ЕСР на валидность.
# Запускается отдельно, но можно интегрировать первым шагом, чтобы остановить выполнения расчётов, либо исключить
# корреспонденции, по которым есть проблема с валидностью ЕСР (отправление / назначение).
# Проверка выполняется путём ввода кода станции в окно R-Тарифа, т.е., фактически - найдёт ли он её.


@logger.catch(reraise=True)
def run_check(df):

    # Создается датафрейм с выделенными столбцами из исходного файла. Столбцы с датой также нужны для объединения.
    df_1 = df[["esr_otpr", "year_for_tariff", "month_for_tariff", "day_for_tariff"]]

    # Создается второй датафрейм с выделенными столбцами из исходного файла. Столбцы с датой также нужны для объединения.
    # Отличие от первого в том, что в первом - станция отправления, во втором - станция назначения.
    df_2 = df[["esr_nazn", "year_for_tariff", "month_for_tariff", "day_for_tariff"]]
    # Переименовывается название столбца, чтобы при объединении данные слились в один столбец.
    df_2 = df_2.rename(columns={"esr_nazn": "esr_otpr"})

    # Объединение данных в один столбец.
    df_3 = concat([df_1, df_2], ignore_index=True, axis=0)
    # Убираются полные дубликаты полученных строк, по которым совпадает: ЕСР и дата расчёта.
    # Итого должен остаться датафрейм с уникальной связкой: ЕСР+дата расчёта Важно, потому что в другие даты расчёта
    # невалидный ЕСР может быть валидным!
    df_3 = df_3.drop_duplicates(ignore_index=True)

    # Выбран SET чтобы дубли сами удалялись при наполнении
    problem_esr = {}

    for i in tqdm(range(0, df_3.shape[0])):

        # Активируется окно RT
        SetRailTariffWindowActive()

        # Переключается раскладка на английскую независимо от текущей, нужно для корректного ввода с клавиатуры
        # и чтобы не искать какая сейчас стоит раскладка.
        change_foreground_window_keyboard_layout(0x04090409)

        sleep(sleep_moment)

        keyDown("ctrl")
        keyDown("n")
        keyUp("n")
        keyUp("ctrl")

        sleep(sleep_moment)

        # Установление курсора для установки даты для расчёта в активное окно RT.
        hotkey("ctrl", "d")
        sleep(sleep_moment)
        write(df_3["day_for_tariff"][i], delay=0.01)
        sleep(sleep_moment)
        write(df_3["month_for_tariff"][i], delay=0.01)
        sleep(sleep_moment)
        write(df_3["year_for_tariff"][i], delay=0.01)
        sleep(sleep_moment)
        press("enter")
        sleep(sleep_tic)
        # Вызывается окно для ввода кода станции
        SetRailTariffWindowActiveForInput(1)
        sleep(sleep_long)
        typewrite(df_3["esr_otpr"][i])
        sleep(sleep_long)
        press("enter")
        sleep(sleep_long)
        # После ввода кода станции ищется ID окна для ввода кода станции.
        # Логика такова, что если окно ещё существует (ID не равен 0) - значит код ЕСР неправильный
        # так как после нажатия 'enter' окно не пропало.
        # Здесь "Станция отправления" это заголовок всплывающего в RT окна.
        wnd = FindWindow(None, "Станция отправления")
        if wnd != 0:
            # print("Проблема со станцией: ", df_3['esr_otpr'][i])
            # Добавляем в словарь код станции и дату расчёта, которые нужно исключить из перечня.
            problem_esr[df_3["esr_otpr"][i]] = df_3["year_for_tariff"][i]
            press("esc")
            sleep(sleep_moment)

        sleep(sleep_long)

    # Преобразован в список списков для удобства в дальнейшем
    problem_esr_lst = [[key, value] for key, value in problem_esr.items()]

    return problem_esr_lst
