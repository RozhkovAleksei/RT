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

from loguru import logger
import asyncio

from RelatedFunctionsAndVariables.externals import sheet_name, end_path_to_source_file, end_path_to_folder_for_detailed_data
from RelatedFunctionsAndVariables.globals import SetDiskLabelByScreenRes
from RelatedFunctionsAndVariables.source_file_funcs import dataframe_preps
from core import run

# Настройка логгера
logger.remove()
logger.add(lambda msg: print(msg), level="ERROR", backtrace=True, diagnose=True)

async def main():

    # Адрес файла с корреспонденциями.
    source_file = SetDiskLabelByScreenRes() + end_path_to_source_file
    details_folder = SetDiskLabelByScreenRes() + end_path_to_folder_for_detailed_data

    try:

        # Подготовка датафрейма для дальнейшей работы, чистка от дублирующихся кодов, коррекция точка-запятая
        cleared_df = dataframe_preps(source_file)

        await run(source_file, details_folder, sheet_name, cleared_df)

    except Exception as e:
        logger.exception(e)
        raise

@logger.catch(reraise=True)
def go_main():
    asyncio.run(main())

if __name__ == '__main__':
    go_main()
