import sys
from datetime import datetime

import pandas as pd
from loguru import logger

from related_funcs_and_variables import check_ESR_by_RT as cesr_rt
from related_funcs_and_variables import check_car_by_RT as ccar_rt
from related_funcs_and_variables.externals import (
    db_filename,
    sheet_name,
    table_name,
    default_full_train_cars_amount,
    default_car_dead_weight,
)
from sql_functions.sql_functions import (
    create_table_if_not_exist_and_check_for_duplicates,
)


@logger.catch(reraise=True)
def dataframe_preps(source_file):

    # Чтобы дебажная печать dataframe влезала без скрытых значений
    pd.set_option("display.width", 320)
    pd.set_option("display.max_columns", 100)

    # Перегоняется в dataframe excel файл с корреспонденциями и обрабатываются запятые в дробных числах,
    df = pd.read_excel(source_file, sheet_name=sheet_name, dtype=str)

    # Немного причесывается dataframe.
    df.year_for_tariff = df.year_for_tariff.fillna(datetime.now().strftime("%Y"))
    df.month_for_tariff = df.month_for_tariff.fillna(datetime.now().strftime("%m"))
    df.day_for_tariff = df.day_for_tariff.fillna(datetime.now().strftime("%d"))
    df.car_dead_weight = df.car_dead_weight.fillna(default_car_dead_weight)
    df.is_container_train = df.is_container_train.fillna("0")
    df.type_of_container = df.type_of_container.fillna("0")
    # Предположение о том, что если столбец изначально пустой, значит тип отправки - М, значит по дефолту М = 71 вагон
    df.cars_amount_in_train = df.cars_amount_in_train.fillna(
        default_full_train_cars_amount
    )
    df.specific_van_for_coal_id = df.specific_van_for_coal_id.fillna("0")

    # Убираются запятые
    df.car_dead_weight = df.car_dead_weight.str.replace(",", ".")
    # Защита от ошибок ручного ввода типа 70,3,5 (а должно быть 70,3), заодно отбрасывается дробная часть
    df.car_dead_weight = pd.to_numeric(df.car_dead_weight, downcast="signed")
    # Преобразование обратно в строку, так как далее будем работать как со строковым значением
    df.car_dead_weight = df.car_dead_weight.astype(str)

    # Убираются запятые
    df.mass_in_car = df.mass_in_car.str.replace(",", ".")
    # Защита от ошибок ручного ввода типа 70,3,5 (а должно быть 70,3)
    df.mass_in_car = pd.to_numeric(df.mass_in_car, downcast="signed")
    # Преобразование обратно в строку, так как далее будем работать как со строковым значением
    df.mass_in_car = df.mass_in_car.astype(str)

    # Проверка на наличие в БД данных, рассчитанных ранее в рамках предыдущих запросов и удаление, если есть.
    # Также, если БД нет - создаётся БД с пустой таблицей
    cleared_df = create_table_if_not_exist_and_check_for_duplicates(
        df, db_filename, table_name
    )

    if len(cleared_df) == 0:
        print("Новых данных нет, работа программы завершена")
        sys.exit()

    # Освобождается память, так как dataframe может быть огромных размеров, незачем держать.
    del df

    # TODO: доделать очистку списка корреспонденций по невалидным вагонам
    # # Если новые данные есть, то перед основным блоком выполняется проверка корректности типа вагона, невалидные в список
    # cars_to_exclude = ccar_rt.run_check(cleared_df)
    # print("Проблемные вагоны ", cars_to_exclude)


    # ...и проверка ЕСР на валидность, невалидные в список
    esr_to_exclude = cesr_rt.run_check(cleared_df)
    # esr_to_exclude = [['02915', '2025'], ['02837', '2025'], ['07843', '2025'], ['07714', '2025'], ['214055', '2025'], ['05980', '2025'], ['02181', '2025'], ['08324', '2025'], ['08999', '2025'], ['09471', '2025'], ['09795', '2025'], ['07703', '2025'], ['19941', '2025'], ['200303', '2025']]
    # esr_to_exclude = [['920040', '2025']]
    # esr_to_exclude = [['044954', '2025'], ['181761', '2025']]
    # esr_to_exclude = [['044954', '2025'], ['194314', '2025'], ['610101', '2025'], ['478102', '2025']]
    # esr_to_exclude = [['425317', '2025'], ['424511', '2025'], ['610101', '2025']]
    # esr_to_exclude = [['657841', '2025'], ['548216', '2025'], ['509005', '2025'], ['506209', '2025'], ['508007', '2025'], ['507108', '2025'], ['472604', '2025'], ['471809', '2025'], ['474608', '2025'], ['470505', '2025'], ['484009', '2025'], ['494800', '2025'], ['144419', '2025']]
    print("Проблемные пары ЕСР - год ", esr_to_exclude)

    # Если список esr_to_exclude не пустой - нужно удалить из датафрейма строки, в которых есть невалидные ЕСР
    if len(esr_to_exclude) != 0:

        for i in esr_to_exclude:
            # print("Текущая рассматриваемая станция и год из невалидных ЕСР: ", i[0], i[1])
            for j in cleared_df.itertuples():
                if (i[0] == j[1] and i[1] == j[13]) or (i[0] == j[3] and i[1] == j[13]):
                    cleared_df.drop(index=j[0], inplace=True)

    return cleared_df

