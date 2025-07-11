from win32gui import FindWindow
from pandas import read_excel, concat
from globals import SetRailTariffWindowActive, SetRailTariffWindowActiveForInput
from pyautogui import hotkey, press, typewrite, keyUp, keyDown
from time import sleep
from py_win_keyboard_layout import change_foreground_window_keyboard_layout
from keyboard import write
from tqdm import tqdm

# Блок для проверки кода станции ЕСР на валидность.
# Запускается отдельно, но можно интегрировать первым шагом, чтобы остановить выполнения расчётов, либо исключить
# корреспонденции, по которым есть проблема с валидностью ЕСР (отправление / назначение).
# Проверка выполняется путём ввода кода станции в окно R-Тарифа, т.е., фактически - найдёт ли он её.

# def RunCheck(source_file, sheet_name):
def RunCheck(df):
    # Перегоняется в dataframe файл с корреспонденциями
    # df = read_excel(source_file, sheet_name=sheet_name, index_col= False, dtype=str)

    # Создается датафрейм с выделенными столбцами из исходного файла. Столбцы с датой также нужны для объединения.
    df_1 = df[['esr_otpr', 'year_for_tariff', 'month_for_tariff', 'day_for_tariff']]
    # Создается второй датафрейм с выделенными столбцами из исходного файла. Столбцы с датой также нужны для объединения.
    # ОТличие от первого в том, что в первом - станция отправления, во втором - станция назначения.
    df_2 = df[['esr_nazn', 'year_for_tariff', 'month_for_tariff', 'day_for_tariff']]
    # Переименовывается название столбца, чтобы при объединении данные слились в один столбец.
    df_2 = df_2.rename(columns={'esr_nazn': 'esr_otpr'})
    # Объединение данных в один столбец.
    df_3 = concat([df_1, df_2], ignore_index=True, axis=0)
    # Убираются полные дубликаты полученных строк, по которым совпадает: ЕСР и дата расчёта.
    # Итого должен остаться датафрейм с уникальной связкой: ЕСР+дата расчёта Важно, потому что в другие даты расчёта
    # невалидный сегодня ЕСР может быть валидным!
    df_3 = df_3.drop_duplicates(ignore_index=True)

    # Сделан SET чтобы дубли сами удалялись
    problem_ESR = {}

    for i in tqdm(range(0, df_3.shape[0])):

        # Переключается раскладка на английскую независимо от текущей, нужно для корректного ввода с клавиатуры
        # и чтобы не искать какая сейчас стоит раскладка.
        change_foreground_window_keyboard_layout(0x04090409)

        # Активируется окно RT
        SetRailTariffWindowActive()

        keyDown('ctrl')
        keyDown('n')
        keyUp('n')
        keyUp('ctrl')

        # Установление курсора для установки даты для расчёта в активное окно RT.
        hotkey('ctrl', 'd')
        sleep(0.2)
        write(str(df_3['day_for_tariff'][i]), delay=0.01)
        sleep(0.2)
        write(str(df_3['month_for_tariff'][i]), delay=0.01)
        sleep(0.2)
        write(str(df_3['year_for_tariff'][i]), delay=0.01)
        sleep(0.2)
        press('enter')
        sleep(0.1)
        # Вызывается окно для ввода кода станции
        SetRailTariffWindowActiveForInput(1)
        sleep(0.5)
        typewrite(str(df_3['esr_otpr'][i]))
        sleep(0.5)
        press('enter')
        sleep(0.3)
        # После ввода кода станции ищется ID окна для ввода кода станции.
        # Логика такова, что если окно ещё существует (ID не равен 0) - значит код ЕСР неправильный!
        wnd = FindWindow(None, "station_otpr_name")
        if wnd != 0:
            print("Проблема со станцией: ", df_3['esr_otpr'][i])
            # Добавляем в словарь код станции и дату расчёта, которые нужно исключить из перечня.
            problem_ESR[df_3['esr_otpr'][i]] = df_3['year_for_tariff'][i]
            press('esc')
            sleep(0.2)

        sleep(0.5)

    # Преобразован в список для удобства в дальнейшем
    problem_ESR_lst = list(problem_ESR)

    # МЫ ПОТЕРЯЛИ ДАТУ ПЛОХОГО ЕСР!!! НАДО ВСЁ ПЕРЕДЕЛЫВАТЬ!

    return problem_ESR_lst
