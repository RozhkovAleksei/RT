import sqlite3
import os
import pandas as pd
from loguru import logger


@logger.catch(reraise=True)
def create_table_if_not_exist_and_check_for_duplicates(dataframe:pd.DataFrame, db_file_name:str, db_table_name:str):

    # Проверка - если файла БД нет - то и проверять незачем. Предположение, что файл БД всегда только один.
    if not os.path.isfile(db_file_name):
        print("check_if_exists - no DB file found -> create empty table")

        connection = sqlite3.connect(db_file_name)
        cursor = connection.cursor()

        # Создание таблицы
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {db_table_name} 
            (
            esr_otpr TEXT,
            station_otpr_name TEXT,
            esr_nazn TEXT,
            station_nazn_name TEXT,
            type_dispatch TEXT,
            is_container_train TEXT,
            etsng_cargo TEXT,
            mass_in_car TEXT,
            type_of_container TEXT,
            type_of_car TEXT,
            car_dead_weight TEXT,
            cars_amount_in_train TEXT,
            year_for_tariff TEXT,
            month_for_tariff TEXT,
            day_for_tariff TEXT,
            specific_van_for_coal_id TEXT,
            mainland_payment_by_loaded_carriage TEXT,
            mainland_payment_by_empty_carriage TEXT,
            mainland_payment_distance TEXT,
            sakhalin_payment_by_loaded_carriage TEXT,
            sakhalin_payment_by_empty_carriage TEXT,
            sakhalin_payment_distance TEXT,
            crimea_payment_by_loaded_carriage TEXT,
            crimea_payment_by_empty_carriage TEXT,
            crimea_payment_distance TEXT,
            kazakhstan_payment_by_loaded_carriage TEXT,
            kazakhstan_payment_by_empty_carriage TEXT,
            kazakhstan_payment_distance TEXT,
            litva_payment_by_loaded_carriage TEXT,
            litva_payment_by_empty_carriage TEXT,
            litva_payment_distance TEXT,
            belarus_payment_by_loaded_carriage TEXT,
            belarus_payment_by_empty_carriage TEXT,
            belarus_payment_distance TEXT,
            zhdn_payment_by_loaded_carriage TEXT,
            zhdn_payment_by_empty_carriage TEXT,
            zhdn_payment_distance TEXT,
            mainland_currency_of_result TEXT,
            sakhalin_currency_of_result TEXT,
            crimea_currency_of_result TEXT,
            kazakhstan_currency_of_result TEXT,
            litva_currency_of_result TEXT,
            belarus_currency_of_result TEXT,
            zhdn_currency_of_result TEXT,
            date_calculation TEXT,
            ETSNG_to_avoid TEXT,
            station_otpr_name_in_system TEXT,
            station_nazn_name_in_system TEXT,
            station_otpr_subject_RF TEXT,
            station_otpr_region TEXT,
            station_otpr_polygon TEXT,
            station_nazn_subject_RF TEXT,
            station_nazn_region TEXT,
            station_nazn_polygon TEXT)
        """)
        connection.commit()
        connection.close()

        return dataframe

    # Если таблица найдена
    df_indexes_of_duplicates = []

    for i in dataframe.itertuples():

        index_of_duplicate = tuple("-1",)

        try:
            with sqlite3.connect(db_file_name) as connection:
                # В index_of_duplicate заполняются индексы из БД корреспонденций, дублирующихся с уже имеющимися в df.
                # При наличии хотя бы одной дублирующейся корреспонденции - последним элементом возвращаемого кортежа
                # будет None, надо предусмотреть обработку.
                # [i, x] - i номер строки, x - номер столбца в dataframe.
                index_of_duplicate=(
                    connection.cursor().execute(
                    'SELECT ROWID FROM ' + '"' + db_table_name + '"' +
                    ' WHERE "esr_otpr" = ' + '"' + dataframe.iat[i[0], 0] + '"'
                    + ' AND "station_otpr_name" = ' + '"' + dataframe.iat[i[0], 1] + '"'
                    + ' AND "esr_nazn" = ' + '"' + dataframe.iat[i[0], 2] + '"'
                    + ' AND "station_nazn_name" = ' + '"' + dataframe.iat[i[0], 3] + '"'
                    + ' AND "type_dispatch" = ' + '"' + dataframe.iat[i[0], 4] + '"'
                    + ' AND "etsng_cargo" = ' + '"' + dataframe.iat[i[0], 6] + '"'
                    + ' AND "type_of_car" = ' + '"' + dataframe.iat[i[0], 9] + '"'
                    + ' AND "year_for_tariff" = ' + '"' + dataframe.iat[i[0], 12] + '"'
                    + ' AND "month_for_tariff" = ' + '"' + dataframe.iat[i[0], 13] + '"'
                    + ' AND "day_for_tariff" = ' + '"' + dataframe.iat[i[0], 14] + '"').fetchone())

        except sqlite3.Error as exp:
            print("Ошибка получения данных для проверки на наличие среди имеющихся: ", exp)

        # -1, так как 0 может оказаться валидным значением
        if index_of_duplicate is None:
            continue
        if index_of_duplicate[0] != -1:
            df_indexes_of_duplicates.append(i[0])

    df_clear = dataframe.drop(index=df_indexes_of_duplicates)

    return df_clear

# В итоге нигде не используется
# def get_available_row_index_in_DB(db_file_name:str, db_table_name:str):
#
#     # Проверка - если файла БД нет - то возвращается 1. Предположение, что файл БД всегда только один.
#     if not os.path.isfile(db_file_name):
#         print("get_available_row_index_in_DB - No DB file found")
#         # 1 потому что ROWID с индексом 0 (по крайней мере в DBViewer показывает строку заголовка)
#         return 1
#
#     try:
#         with sqlite3.connect(db_file_name) as connection:
#             available_index = connection.cursor().execute(
#                 'SELECT MAX(ROWID) FROM '+'"' + db_table_name + '"').fetchone()[0]
#     except sqlite3.Error as exp:
#         print("Ошибка получения данных о последней записи в базе данных: ", exp)
#
#     available_index = int(available_index) + 1
#
#     return available_index