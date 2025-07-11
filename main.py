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

import sys
from pandas import read_excel, to_numeric
import sqlite3
import Run as run
from globals import SetDiskLabelByScreenRes, dtype_mapping, check_if_exists
from externals import end_path_to_source_file, end_path_to_folder_for_detailed_data, db_filename, table_name, sheet_name
import get_stations_data_by_DB as gsdb
import check_ESR_by_RT as cesr

if __name__ == '__main__':

    # Адрес файла с корреспонденциями.
    source_file = SetDiskLabelByScreenRes() + end_path_to_source_file
    details_folder = SetDiskLabelByScreenRes() + end_path_to_folder_for_detailed_data

    # Перегоняется в dataframe excel файл с корреспонденциями и обрабатываются запятые в дробных числах,
    # в качестве заголовков столбцов используется 2 строка исходного файла (header=1)
    df = read_excel(source_file, sheet_name=sheet_name, dtype=str)
    df.car_dead_weight = df.car_dead_weight.str.replace(',', '.')
    df.car_dead_weight = to_numeric(df.car_dead_weight, downcast='signed')
    df.car_dead_weight = df.car_dead_weight.astype(str)
    df.mass_in_car = df.mass_in_car.str.replace(',', '.')
    df.mass_in_car = to_numeric(df.mass_in_car, downcast='signed')
    df.mass_in_car = df.mass_in_car.astype(str)

    # Заполняются пустые значения в датах расчёта
    df.year_for_tariff = df.year_for_tariff.fillna('не указан')
    df.month_for_tariff = df.month_for_tariff.fillna('не указан')
    df.day_for_tariff = df.day_for_tariff.fillna('не указан')

    # Проверка на наличие БД данных, рассчитанных ранее в рамках предыдущих запросов.
    cleared_df = check_if_exists(df, db_filename, table_name)
    # print(cleared_df)

    if len(cleared_df) == 0:
        print("Новых данных нет, работа программы завершена")
        sys.exit()

    # Если новые данные есть, то перед основным блоком выполняется проверка ЕСР на валидность, невалидные в список
    ESR_to_exclude = cesr.RunCheck(cleared_df)
    # case 1: список пустой - проходим дальше
    # case 2: список не пустой - нужно удаить из датафрейма строки, в которых есть невалидные ЕСР
    if len(ESR_to_exclude) != 0:
        print("Список станций ЕСР, исключенных из расчёта: ", ESR_to_exclude)

        # for i in ESR_to_exclude:
        #     print(i)
        #     if len(df) != 0:
        #         print("in if")
        #         for j in df['esr_otpr']:
        #             print(df['esr_otpr'][j])
        #             if i == j:
        #                 print("drop:", j)
        #                 df.drop(index=j)
        #                 print(len(df))
        #         for k in df['esr_nazn']:
        #             print(df['esr_nazn'][k])
        #             if i == k:
        #                 print("drop:", k)
        #                 df.drop(index=k)
        #                 print(len(df))

    # Подтягивается из БД дополнительная информация о станциях отправления/назначения
    stations_meta = gsdb.GetActualStationsDataCheckValidDataAndGetPreferences(cleared_df)
    # Если нужно временно отключить подтягивание из БД доп.данных, ничего не сломается, просто не будет доп.инфо.
    # stations_meta_data = []

    # По факту pandas примет всё как str, несмотря на globals.dtype_mapping, для правки - надо весь импорт в dataframe переделать
    # Но это за собой потащит такие изменения как невозможность без промежуточной конвертации в строку - имитировать
    # ввод с клавиатуры цифр, либо работать через буфер обмена на вставку готового значения.
    try:
        with sqlite3.connect(db_filename) as connection:

            # Проверка подключения к базе данных
            if connection is None:
                raise ConnectionError("Проблема с подключением к базе данных")

            cleared_df.to_sql(table_name, connection, if_exists='append', index=True, dtype=dtype_mapping)
            # df.to_sql(table_name, connection, if_exists='replace', index=True, dtype=dtype_mapping)
            connection.commit()

    except sqlite3.Error as exp:
        print("Ошибка при создании таблицы:", exp)

    run.Run(source_file, details_folder, sheet_name, cleared_df, stations_meta, ESR_to_exclude)

