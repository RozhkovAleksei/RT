# Данная программа автоматизирует расчёт тарифов путем взаимодействия с интерфейсом программы RT.
# Логика работы следующая: в отдельном файле Excel поступают заранее размеченные данные о корреспонденциях.
# Эти данные подгружаются в датафрейм (pandas) и на основе данных каждой строки происходит параметризация запроса к RT.
# Для исключения ошибок в поступивших данных происходит их валидация через проверку на то, что коды существуют.
# Каждая корреспонденция дополняется информацией о географическом расположении станций и принадлежности к региону.
# Взаимодействие с RT осуществляется посредством имитации ручного ввода в интерфейс программы RT.
# Имитация ручного ввода организована через управление клавиатурой и поиском отдельных элементов на экране (OpenCV).
# Результат полученных данных из RT записывается в датафрейм и в отдельные выгрузки Excel.
# Итоговый датафрейм выгружается в исходный файл Excel, дополняя его данными из RT.
# Также данные собираются в БД на sqlite3 для кэширования.
# Программа организована так.
# Создан объект с полями, соответствующими всем параметрам корреспонденции.
# Созданы отдельные модули, различающиеся по взаимодействию с RT.
# Запуск цикла по длине датафрейма, в котором на каждой итерации осуществляется по-очередный вызов модулей.
# Ключевая сложность заключается в том, что по основным операциям, связанным с взаимодействием с окном программы RT
# почти нигде невозможно на уровне программы (кода) получить подтверждение об успешности выполненного действия.
# В связи с этим, фактически, программа работает на ожидании успешности выполняемых операций с заложенными подстраховками.

import pandas as pd
import sys
from datetime import datetime
from loguru import logger
from globals import SetDiskLabelByScreenRes
from sql_functions import create_table_if_not_exist_and_check_for_duplicates
from externals import end_path_to_source_file, end_path_to_folder_for_detailed_data, db_filename, table_name, sheet_name
import get_stations_data_by_DB as gsdb
import check_ESR_by_RT as cesr_rt
from core import run

# Настройка логгера
logger.remove()
logger.add(lambda msg: print(msg), level="ERROR", backtrace=True, diagnose=True)

def main():

    try:
        # Чтобы дебажная печать dataframe влезала без скрытых значений
        pd.set_option('display.width', 320)
        pd.set_option('display.max_columns', 100)

        # Адрес файла с корреспонденциями.
        source_file = SetDiskLabelByScreenRes() + end_path_to_source_file
        details_folder = SetDiskLabelByScreenRes() + end_path_to_folder_for_detailed_data

        # Перегоняется в dataframe excel файл с корреспонденциями и обрабатываются запятые в дробных числах,
        df = pd.read_excel(source_file, sheet_name=sheet_name, dtype=str)

        # Немного причесывается dataframe.
        df.car_dead_weight = df.car_dead_weight.fillna("0")
        df.year_for_tariff = df.year_for_tariff.fillna(datetime.now().strftime("%Y"))
        df.month_for_tariff = df.month_for_tariff.fillna(datetime.now().strftime("%m"))
        df.day_for_tariff = df.day_for_tariff.fillna(datetime.now().strftime("%d"))
        df.is_container_train = df.is_container_train.fillna("0")
        df.type_of_container = df.type_of_container.fillna("0")
        df.cars_amount_in_train = df.cars_amount_in_train.fillna("0")
        df.specific_van_for_coal_id = df.specific_van_for_coal_id.fillna("0")

        # Убираются запятые
        df.car_dead_weight = df.car_dead_weight.str.replace(',', '.')
        # Защита от ошибок ручного ввода типа 70,3,5 (а должно быть 70,3), заодно отбрасывается дробная часть
        df.car_dead_weight = pd.to_numeric(df.car_dead_weight, downcast='signed')
        # Преобразование обратно в строку, так как далее будем работать как со строковым значением
        df.car_dead_weight = df.car_dead_weight.astype(str)

        # Убираются запятые
        df.mass_in_car = df.mass_in_car.str.replace(',', '.')
        # Защита от ошибок ручного ввода типа 70,3,5 (а должно быть 70,3)
        df.mass_in_car = pd.to_numeric(df.mass_in_car, downcast='signed')
        # Преобразование обратно в строку, так как далее будем работать как со строковым значением
        df.mass_in_car = df.mass_in_car.astype(str)

        # Проверка на наличие в БД данных, рассчитанных ранее в рамках предыдущих запросов и удаление, если есть.
        # Также, если БД нет - создаётся БД с пустой таблицей
        cleared_df = create_table_if_not_exist_and_check_for_duplicates(df, db_filename, table_name)

        if len(cleared_df) == 0:
            print("Новых данных нет, работа программы завершена")
            sys.exit()

        # Освобождается память, так как dataframe может быть огромных размеров, незачем держать.
        del df

        # Если новые данные есть, то перед основным блоком выполняется проверка ЕСР на валидность, невалидные в список
        ESR_to_exclude = cesr_rt.RunCheck(cleared_df)
        # ESR_to_exclude = [['200303', '2025']]
        print("Проблемные пары ЕСР - год ", ESR_to_exclude)

        # Если список не пустой - нужно удалить из датафрейма строки, в которых есть невалидные ЕСР
        if len(ESR_to_exclude) != 0:

            for i in ESR_to_exclude:
                # print("Текущая рассматриваемая станция и год из невалидных ЕСР: ", i[0], i[1])
                for j in cleared_df.itertuples():
                    if (i[0] == j[1] and i[1] == j[13]) or (i[0] == j[3] and i[1] == j[13]):
                        cleared_df.drop(index=j[0], inplace=True)

        # Подтягивается из БД дополнительная информация о станциях отправления/назначения, хранится в массиве данных
        stations_meta = gsdb.GetAdditionalDataAboutStations(cleared_df)
        # Если нужно временно отключить подтягивание из БД доп.данных, ничего не сломается, просто не будет доп.инфо.
        # stations_meta_data = []

        run(source_file, details_folder, sheet_name, cleared_df, stations_meta)

    except Exception as e:
        logger.exception(e)
        raise

@logger.catch(reraise=True)
def go_main():
    main()

if __name__ == '__main__':
    go_main()