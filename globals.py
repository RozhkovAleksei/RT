from pyautogui import keyDown, keyUp, press
from pygetwindow import getWindowsWithTitle
from time import sleep
import sys
from pandas import ExcelWriter
from datetime import datetime
from py_win_keyboard_layout import change_foreground_window_keyboard_layout
from win32api import GetSystemMetrics
import win32gui
import pyscreeze
import sqlite3

# Класс для создания общего объекта, который хранит в себе все результаты расчётов по i-й корреспонденции.
# Класс создан для удобства обращения к полям при переходе выполнения программы из одного модуля - в другой.
class my_obj:
    def __init__(self):
        # self.confid = 0.742
        self.min_search_time = 0
        self.calc_year = 0
        self.calc_month = 0
        self.calc_day = 0
        self.date_calculation = ''
        self.is_full_train_containers = 0
        self.mainland_payment_by_loaded_carriage = 0
        self.mainland_payment_by_empty_carriage = 0
        self.mainland_payment_distance = 0
        self.sakhalin_payment_by_loaded_carriage = 0
        self.sakhalin_payment_by_empty_carriage = 0
        self.sakhalin_payment_distance = 0
        self.crimea_payment_by_loaded_carriage = 0
        self.crimea_payment_by_empty_carriage = 0
        self.crimea_payment_distance = 0
        self.kazakhstan_payment_by_loaded_carriage = 0
        self.kazakhstan_payment_by_empty_carriage = 0
        self.kazakhstan_payment_distance = 0
        self.litva_payment_by_loaded_carriage = 0
        self.litva_payment_by_empty_carriage = 0
        self.litva_payment_distance = 0
        self.belarus_payment_by_loaded_carriage = 0
        self.belarus_payment_by_empty_carriage = 0
        self.belarus_payment_distance = 0
        self.zhdn_payment_by_loaded_carriage = 0
        self.zhdn_payment_by_empty_carriage = 0
        self.zhdn_payment_distance = 0
        self.mainland_currency_of_result = "RUB"
        self.sakhalin_currency_of_result = "RUB"
        self.crimea_currency_of_result = "RUB"
        self.zhdn_currency_of_result = "RUB"
        self.kazakhstan_currency_of_result = "CHF"
        self.litva_currency_of_result = "CHF"
        self.belarus_currency_of_result = "CHF"
        self.specific_van_for_coal_id = ' '
        self.duration_for_test_purposes = 0
        self.log_data = ''
        self.is_ESR_correct = 1
        self.path_to_img_data = " "
        self.global_sleep_long = 0.5
        self.global_sleep_short = 0.3
        self.global_sleep_moment = 0.2
        self.ETSNG_to_avoid = ''
        self.station_otpr_name_in_system=''
        self.station_otpr_subject_RF = ''
        self.station_otpr_region = ''
        self.station_otpr_polygon = ''
        self.station_nazn_name_in_system=''
        self.station_nazn_subject_RF = ''
        self.station_nazn_region = ''
        self.station_nazn_polygon = ''

    # По уму надо бы сделать get set ещё, но инкапсуляция в питоне по дефолту - не особо.

    def print_attrs(self):
        print("mainland_payment_by_loaded_carriage: ", self.mainland_payment_by_loaded_carriage)
        print("mainland_payment_by_empty_carriage: ", self.mainland_payment_by_empty_carriage)
        print("mainland_payment_distance: ", self.mainland_payment_distance)
        print("sakhalin_payment_by_loaded_carriage: ", self.sakhalin_payment_by_loaded_carriage)
        print("sakhalin_payment_by_empty_carriage: ", self.sakhalin_payment_by_empty_carriage)
        print("sakhalin_payment_distance: ", self.sakhalin_payment_distance)
        print("crimea_payment_by_loaded_carriage: ", self.crimea_payment_by_loaded_carriage)
        print("crimea_payment_by_empty_carriage: ", self.crimea_payment_by_empty_carriage)
        print("crimea_payment_distance: ", self.crimea_payment_distance)
        print("kazakhstan_payment_by_loaded_carriage: ", self.kazakhstan_payment_by_loaded_carriage)
        print("kazakhstan_payment_by_empty_carriage: ", self.kazakhstan_payment_by_empty_carriage)
        print("kazakhstan_payment_distance: ", self.kazakhstan_payment_distance)
        print("litva_payment_by_loaded_carriage: ", self.litva_payment_by_loaded_carriage)
        print("litva_payment_by_empty_carriage: ", self.litva_payment_by_empty_carriage)
        print("litva_payment_distance: ", self.litva_payment_distance)
        print("belarus_payment_by_loaded_carriage: ", self.belarus_payment_by_loaded_carriage)
        print("belarus_payment_by_empty_carriage: ", self.belarus_payment_by_empty_carriage)
        print("belarus_payment_distance: ", self.belarus_payment_distance)
        print("zhdn_payment_by_loaded_carriage: ", self.zhdn_payment_by_loaded_carriage)
        print("zhdn_payment_by_empty_carriage: ", self.zhdn_payment_by_empty_carriage)
        print("zhdn_payment_distance: ", self.zhdn_payment_distance)
        print("mainland_currency_of_result: ", self.mainland_currency_of_result)
        print("sakhalin_currency_of_result: ", self.sakhalin_currency_of_result)
        print("crimea_currency_of_result: ", self.crimea_currency_of_result)
        print("zhdn_currency_of_result: ", self.zhdn_currency_of_result)
        print("kazakhstan_currency_of_result: ", self.kazakhstan_currency_of_result)
        print("litva_currency_of_result: ", self.litva_currency_of_result)
        print("belarus_currency_of_result: ", self.belarus_currency_of_result)

    def __del___(self):
        pass

# Функция для того, чтобы сделать активным окно программы RT
def SetRailTariffWindowActive():
    # Переключается раскладка на английскую независимо от текущей, нужно для ввода с клавиатуры
    change_foreground_window_keyboard_layout(0x04090409)

    sleep(0.2)

    try:
        rail_tariff_window = getWindowsWithTitle('Новый расчёт - R-Тариф')[0]
        sleep(0.5)
        if rail_tariff_window.isActive is not True:
            rail_tariff_window.activate()
            sleep(0.5)
    except:
        print(SetRailTariffWindowActive.__name__, ' проблема - не найдено окно R-Тариф')
        sys.exit()

# Функция для того, чтобы сделать активным окно программы RT и запустить комбинацию горячих клавиш
def SetRailTariffWindowActiveForInput(hotkey_number):

    sleep(0.2)

    try:
        SetRailTariffWindowActive()

        # Ввод горячих клавиш для открытия соответствующих окон для ввода параметров расчета
        keyDown('ctrl')
        sleep(0.15)
        press(str(hotkey_number))
        sleep(0.15)
        keyUp('ctrl')
        sleep(0.2)
    except:
        print(SetRailTariffWindowActiveForInput.__name__, ' проблема - не найдено окно для ввода')
        sys.exit()

# Когда что-то пошло не так, то нужен выход с гарантией выхода, потому что зависает и теряет окно в непредсказуемых местах
def ExitByError():
    print(ExitByError.__name__)
    SetRailTariffWindowActive()
    sleep(0.5)
    press('esc')
    sleep(0.5)
    press('esc')
    sleep(0.5)
    press('esc')
    sleep(0.5)
    press('tab')
    sleep(0.5)
    press('esc')
    sleep(0.5)
    sys.exit()


# Блок для определения отдельных параметров, в зависимости от локального компьютера, на котором происходит проверка
# Big monitor resolution:
# 3840 x 1600
# Small monitor resolution:
# 1920 x 1080
# scr_width GetSystemMetrics(0)
# scr_height GetSystemMetrics(1)
def SetPathToImgByScreenRes():

    screen_res = [GetSystemMetrics(0), GetSystemMetrics(1)]
    if screen_res[0] != 1920:
        return "ImgData/HighRes/"
    else:
        return "ImgData/"

def SetDiskLabelByScreenRes():

    screen_res = [GetSystemMetrics(0), GetSystemMetrics(1)]
    if screen_res[0] != 1920:
        return "Y"
    else:
        return "Z"

def gng_extra_option_finder(my_object) -> str:

    SetRailTariffWindowActive()

    gng_not_defined_content = None

    gng_defined_content = None

    sleep(my_object.global_sleep_short)

    gng_extra_option_window = win32gui.FindWindow(None, "Классификатор грузов ГНГ")

    gng_extra_option_window_coord = win32gui.GetWindowRect(gng_extra_option_window)

    if gng_extra_option_window is not None:
        try:
            SetRailTariffWindowActive()

            gng_not_defined_content = pyscreeze.locateOnScreen(my_object.path_to_img_data + "GNG_not_defined.png",
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
                                                               # minSearchTime=my_object.min_search_time
                                                                                                        )

        except Exception as gng_not_def_excp:
            # print("ГНГ окно с неопределенным кодом не найдено")
            print("gng_not_def_excp", gng_not_def_excp)

        try:
            SetRailTariffWindowActive()

            gng_defined_content = pyscreeze.locateOnScreen(my_object.path_to_img_data + "GNG_defined.png",
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
                                                               # minSearchTime=my_object.min_search_time
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

def write_results_excel(df, cur_row, mobj, sheet_name, source_file):
    # Заполнение текущей строки датафрейма результатами расчета текущей итерации.
    # cur_row номер строки в датафрейме для позиционирования в файле Excel, 16,17 и тд. - столбец в excel-файле
    df.iat[cur_row, 16] = mobj.mainland_payment_by_loaded_carriage
    df.iat[cur_row, 17] = mobj.mainland_payment_by_empty_carriage
    df.iat[cur_row, 18] = mobj.mainland_payment_distance
    df.iat[cur_row, 19] = mobj.sakhalin_payment_by_loaded_carriage
    df.iat[cur_row, 20] = mobj.sakhalin_payment_by_empty_carriage
    df.iat[cur_row, 21] = mobj.sakhalin_payment_distance
    df.iat[cur_row, 22] = mobj.crimea_payment_by_loaded_carriage
    df.iat[cur_row, 23] = mobj.crimea_payment_by_empty_carriage
    df.iat[cur_row, 24] = mobj.crimea_payment_distance
    df.iat[cur_row, 25] = mobj.kazakhstan_payment_by_loaded_carriage
    df.iat[cur_row, 26] = mobj.kazakhstan_payment_by_empty_carriage
    df.iat[cur_row, 27] = mobj.kazakhstan_payment_distance
    df.iat[cur_row, 28] = mobj.litva_payment_by_loaded_carriage
    df.iat[cur_row, 29] = mobj.litva_payment_by_empty_carriage
    df.iat[cur_row, 30] = mobj.litva_payment_distance
    df.iat[cur_row, 31] = mobj.belarus_payment_by_loaded_carriage
    df.iat[cur_row, 32] = mobj.belarus_payment_by_empty_carriage
    df.iat[cur_row, 33] = mobj.belarus_payment_distance
    df.iat[cur_row, 34] = mobj.zhdn_payment_by_loaded_carriage
    df.iat[cur_row, 35] = mobj.zhdn_payment_by_empty_carriage
    df.iat[cur_row, 36] = mobj.zhdn_payment_distance
    df.iat[cur_row, 37] = mobj.mainland_currency_of_result
    df.iat[cur_row, 38] = mobj.sakhalin_currency_of_result
    df.iat[cur_row, 39] = mobj.crimea_currency_of_result
    df.iat[cur_row, 40] = mobj.kazakhstan_currency_of_result
    df.iat[cur_row, 41] = mobj.litva_currency_of_result
    df.iat[cur_row, 42] = mobj.belarus_currency_of_result
    df.iat[cur_row, 43] = mobj.zhdn_currency_of_result
    df.iat[cur_row, 44] = str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    df.iat[cur_row, 45] = str(mobj.ETSNG_to_avoid)
    df.iat[cur_row, 46] = mobj.station_otpr_name_in_system
    df.iat[cur_row, 48] = mobj.station_otpr_subject_RF
    df.iat[cur_row, 49] = mobj.station_otpr_region
    df.iat[cur_row, 50] = mobj.station_otpr_polygon
    df.iat[cur_row, 47] = mobj.station_nazn_name_in_system
    df.iat[cur_row, 51] = mobj.station_nazn_subject_RF
    df.iat[cur_row, 52] = mobj.station_nazn_region
    df.iat[cur_row, 53] = mobj.station_nazn_polygon

    try:
        # выгрузка в Excel заполненного на данной итерации цикла датасета в папку проекта.
        with ExcelWriter(source_file, mode="a", engine="openpyxl", if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=str(sheet_name + "_result"))
    except Exception as e:
        print(e)
        # print('Проблема записи результатов расчета в файл данных')

def setStationsMetaDataToObject(mobj, stations_meta_data, begin_station, end_station):

    for station_data in stations_meta_data:

        # Ищется сравнение по неполному коду ЕСР, так как в НСИ последний (шестой) знак кода ЕСР не используется
        if str(begin_station)[:-1] == str(station_data[0]):

            mobj.station_otpr_name_in_system = station_data[1]  # Наименование станции отправления в системах
            mobj.station_otpr_subject_RF = station_data[2]  # Принадлежность станции отправления к субъекту РФ
            mobj.station_otpr_region = station_data[3]  # Принадлежность станции отправления к федеральному округу
            mobj.station_otpr_polygon = station_data[4]  # Принадлежность станции отправления к полигону

        # Ищется сравнение по неполному коду ЕСР, так как в НСИ последний (шестой) знак кода ЕСР не используется
        if str(end_station)[:-1] == str(station_data[0]):

            mobj.station_nazn_name_in_system = station_data[1]  # Наименование станции назначения в системах
            mobj.station_nazn_subject_RF = station_data[2]  # Принадлежность станции назначения к субъекту РФ
            mobj.station_nazn_region = station_data[3]  # Принадлежность станции назначения к федеральному округу
            mobj.station_nazn_polygon = station_data[4]  # Принадлежность станции назначения к полигону


# SQLITE3 dtypes INTEGER, REAL, TEXT
dtype_mapping = {
    'esr_otpr': 'TEXT',
    'station_otpr_name': 'TEXT',
    'esr_nazn': 'TEXT',
    'station_nazn_name': 'TEXT',
    'type_dispatch': 'TEXT',
    'is_container_train': 'INTEGER',
    'etsng_cargo': 'TEXT',
    'mass_in_car': 'INTEGER',
    'type_of_container': 'TEXT',
    'type_of_car': 'TEXT',
    'car_dead_weight': 'INTEGER',
    'cars_amount_in_train': 'INTEGER',
    'year_for_tariff': 'TEXT',
    'month_for_tariff': 'TEXT',
    'day_for_tariff': 'TEXT',
    'special_car_type': 'TEXT',
    'mainland_payment_by_loaded_carriage': 'REAL',
    'mainland_payment_by_empty_carriage': 'REAL',
    'mainland_payment_distance': 'INTEGER',
    'sakhalin_payment_by_loaded_carriage': 'REAL',
    'sakhalin_payment_by_empty_carriage': 'REAL',
    'sakhalin_payment_distance': 'INTEGER',
    'crimea_payment_by_loaded_carriage': 'REAL',
    'crimea_payment_by_empty_carriage': 'REAL',
    'crimea_payment_distance': 'INTEGER',
    'kazakhstan_payment_by_loaded_carriage': 'REAL',
    'kazakhstan_payment_by_empty_carriage': 'REAL',
    'kazakhstan_payment_distance': 'INTEGER',
    'litva_payment_by_loaded_carriage': 'REAL',
    'litva_payment_by_empty_carriage': 'REAL',
    'litva_payment_distance': 'INTEGER',
    'belarus_payment_by_loaded_carriage': 'REAL',
    'belarus_payment_by_empty_carriage': 'REAL',
    'belarus_payment_distance': 'INTEGER',
    'zhdn_payment_by_loaded_carriage': 'REAL',
    'zhdn_payment_by_empty_carriage': 'REAL',
    'zhdn_payment_distance': 'INTEGER',
    'mainland_currency_of_result': 'TEXT',
    'sakhalin_currency_of_result': 'TEXT',
    'crimea_currency_of_result': 'TEXT',
    'kazakhstan_currency_of_result': 'TEXT',
    'litva_currency_of_result': 'TEXT',
    'belarus_currency_of_result': 'TEXT',
    'zhdn_currency_of_result': 'TEXT',
    'date_of_calc' : 'TEXT',
    'ETSNG_to_avoid': 'TEXT',
    'station_otpr_name_in_system': 'TEXT',
    'station_nazn_name_in_system': 'TEXT',
    'station_otpr_subject_RF': 'TEXT',
    'station_otpr_region': 'TEXT',
    'station_otpr_polygon': 'TEXT',
    'station_nazn_subject_RF': 'TEXT',
    'station_nazn_region': 'TEXT',
    'station_nazn_polygon': 'TEXT'
}

# Инфо вывод текущей корреспонденции с её параметрами
def cur_state_print(cur_r, dataframe, mobj):

    mobj.log_data = (str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                   + ' ' + str(cur_r + 1) + '/' + str(len(dataframe.index))
                   + ' ' + str(dataframe.iloc[cur_r]['station_otpr_name'])
                   + '-' + str(dataframe.iloc[cur_r]['station_nazn_name'])
                   + ', ТипОтпр - '
                   + str(dataframe.iloc[cur_r]['type_dispatch'])
                   + ', КонтПоезд (0/1)-' + str(dataframe.iloc[cur_r]['is_container_train'])
                   + ', ЕТСНГ-' + str(dataframe.iloc[cur_r]['etsng_cargo'])
                   + ', Масса в вагоне-' + str(dataframe.iloc[cur_r]['mass_in_car'])
                   + ', ТипКонт-' + str(dataframe.iloc[cur_r]['type_of_container'])
                   + ', РодПС-' + str(dataframe.iloc[cur_r]['type_of_car'])
                   + ', Статн.-' + str(dataframe.iloc[cur_r]['car_dead_weight'])
                   + ', Кол-воВагонов-' + str(dataframe.iloc[cur_r]['cars_amount_in_train'])
                   + ', ДатаРасчета-' + mobj.calc_year + '-' + mobj.calc_month + '-' + mobj.calc_day
                   + ', СпецПВ-' + str(dataframe.iloc[cur_r]['special_car_type']))
    print(mobj.log_data, sep=', ')


def check_if_exists(dataframe, db_file, db_table):

    indexes_of_duplicates=[]

    for i in range(len(dataframe)):

        try:
            with sqlite3.connect(db_file) as connection:
                # Заполняются индексы курреспонденций, дублирующихся с уже имеющимися.
                # При наличии хотя бы одной корреспонденции, дублирующейся - послденим элементом будет None
                indexes_of_duplicates.append(connection.cursor().execute(
                    'SELECT "index" FROM ' + '"' + db_table + '"' + ' WHERE "esr_otpr" = ' + '"'
                    + str(dataframe.iat[i, 0]) + '"'
                    + ' AND "esr_nazn" = ' + '"' + str(dataframe.iat[i, 2]) + '"'
                    + ' AND "station_otpr_name" = ' + '"' + str(dataframe.iat[i, 1]) + '"'
                    + ' AND "station_nazn_name" = ' + '"' + str(dataframe.iat[i, 3]) + '"'
                    + ' AND "year_for_tariff" = ' + '"' + str(dataframe.iat[i, 12]) + '"'
                    + ' AND "month_for_tariff" = ' + '"' + str(dataframe.iat[i, 13]) + '"'
                    + ' AND "day_for_tariff" = ' + '"' + str(dataframe.iat[i, 14]) + '"').fetchone())

        except sqlite3.Error as exp:
            print("Ошибка получения данных из базы для проверки на наличие уже имеющиеся: ", exp)

    if len(indexes_of_duplicates) == 0:
        return dataframe

    indexes_of_duplicates_wo_None = tuple(x for x in indexes_of_duplicates if x is not None)

    lst = [list(row) for row in indexes_of_duplicates_wo_None]
    flat_list = sum(lst, [])

    df_clear = dataframe.drop(index=flat_list)

    return df_clear

