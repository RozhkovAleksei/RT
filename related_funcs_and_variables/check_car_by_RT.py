from time import sleep

from keyboard import write
from loguru import logger
from py_win_keyboard_layout import change_foreground_window_keyboard_layout
from pyautogui import hotkey, keyDown, keyUp, press, typewrite
from tqdm import tqdm
from win32gui import FindWindow

from related_funcs_and_variables.externals import sleep_long, sleep_moment, sleep_tic
from related_funcs_and_variables.globals import (
    SetRailTariffWindowActive,
    SetRailTariffWindowActiveForInput,
)


@logger.catch(reraise=True)
def run_check(df):
    '''
    Блок для проверки типа подвижного состава на валидность.
    Запускается отдельно, но можно интегрировать первым шагом, чтобы остановить выполнения расчётов, либо исключить
    корреспонденции, по которым есть проблема с типом подвижного состава.
    Проверка выполняется путём ввода типа подвижного состава в окно R-Тарифа, т.е., фактически - проверка на наличие.
    '''

    # Создается датафрейм с выделенными столбцами из исходного файла.
    df_1 = df[["type_of_car"]]
    df_1.drop_duplicates(inplace=True)

    # Выбран SET чтобы дубли сами удалялись при наполнении
    problem_cars = []

    for i in tqdm(range(0, df_1.shape[0])):

        # Активируется окно RT
        SetRailTariffWindowActive()

        # Переключается раскладка на английскую независимо от текущей, нужно для корректного ввода с клавиатуры
        # и чтобы не искать какая сейчас стоит раскладка.
        change_foreground_window_keyboard_layout(0x04090409)

        sleep(sleep_moment)

        keyDown("ctrl")
        keyDown("6")
        keyUp("6")
        keyUp("ctrl")

        sleep(sleep_moment)

        typewrite(df_1["type_of_car"][i])
        sleep(sleep_long)
        press("enter")
        sleep(sleep_long)
        # После ввода типа подвижного состава ищется ID окна для ввода типа подвижного состава.
        # Логика такова, что если окно ещё существует (ID не равен 0) - значит подвижной состав не найден,
        # так как после нажатия 'enter' окно не пропало.
        # Здесь "Подвижной состав" это заголовок всплывающего в RT окна.
        wnd = FindWindow(None, "Подвижной состав")
        if wnd != 0:
            # print("Проблема со станцией: ", df_3['esr_otpr'][i])
            # Добавляем в словарь код станции и дату расчёта, которые нужно исключить из перечня.
            problem_cars.append(df["type_of_car"][i])
            press("esc")
            sleep(sleep_moment)

        sleep(sleep_long)

    return problem_cars
