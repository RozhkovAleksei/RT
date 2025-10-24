"""Данный модуль содержит функционал выгрузки данных о корреспонденции в БД"""

import sqlite3

from loguru import logger


@logger.catch(reraise=True)
# async def write_corr_result_to_db(mo, db_filename, table_name):
def write_corr_result_to_db(mo, db_filename, table_name):
    """Если первичный запуск и БД нет - создаётся пустая БД с таблицей"""

    with sqlite3.connect(db_filename) as connection:

        # Проверка подключения к базе данных
        if connection is None:
            raise ConnectionError("Проблема с подключением к базе данных")

    try:
        with sqlite3.connect(db_filename) as connection:
            cursor = connection.cursor()

            fields = [
                "esr_otpr",
                "station_otpr_name",
                "esr_nazn",
                "station_nazn_name",
                "type_dispatch",
                "is_container_train",
                "etsng_cargo",
                "mass_in_car",
                "type_of_container",
                "type_of_car",
                "car_dead_weight",
                "cars_amount_in_train",
                "year_for_tariff",
                "month_for_tariff",
                "day_for_tariff",
                "specific_van_for_coal_id",
                "mainland_payment_by_loaded_carriage",
                "mainland_payment_by_empty_carriage",
                "mainland_payment_distance",
                "sakhalin_payment_by_loaded_carriage",
                "sakhalin_payment_by_empty_carriage",
                "sakhalin_payment_distance",
                "crimea_payment_by_loaded_carriage",
                "crimea_payment_by_empty_carriage",
                "crimea_payment_distance",
                "kazakhstan_payment_by_loaded_carriage",
                "kazakhstan_payment_by_empty_carriage",
                "kazakhstan_payment_distance",
                "litva_payment_by_loaded_carriage",
                "litva_payment_by_empty_carriage",
                "litva_payment_distance",
                "belarus_payment_by_loaded_carriage",
                "belarus_payment_by_empty_carriage",
                "belarus_payment_distance",
                "zhdn_payment_by_loaded_carriage",
                "zhdn_payment_by_empty_carriage",
                "zhdn_payment_distance",
                "mainland_currency_of_result",
                "sakhalin_currency_of_result",
                "crimea_currency_of_result",
                "kazakhstan_currency_of_result",
                "litva_currency_of_result",
                "belarus_currency_of_result",
                "zhdn_currency_of_result",
                "date_calculation",
                "ETSNG_to_avoid",
                "station_otpr_name_in_system",
                "station_nazn_name_in_system",
                "station_otpr_subject_RF",
                "station_otpr_region",
                "station_otpr_polygon",
                "station_nazn_subject_RF",
                "station_nazn_region",
                "station_nazn_polygon",
            ]

            placeholders = ", ".join(["?"] * len(fields))
            quoted_fields = ", ".join([f'"{f}"' for f in fields])
            query = (
                f'INSERT INTO "{table_name}" ({quoted_fields}) VALUES ({placeholders})'
            )

            # print(query)

            values = [
                mo.esr_otpr,
                mo.station_otpr_name,
                mo.esr_nazn,
                mo.station_nazn_name,
                mo.type_dispatch,
                mo.is_container_train,
                mo.etsng_cargo,
                mo.mass_in_car,
                mo.type_of_container,
                mo.type_of_car,
                mo.car_dead_weight,
                mo.cars_amount_in_train,
                mo.year_for_tariff,
                mo.month_for_tariff,
                mo.day_for_tariff,
                mo.specific_van_for_coal_id,
                mo.mainland_payment_by_loaded_carriage,
                mo.mainland_payment_by_empty_carriage,
                mo.mainland_payment_distance,
                mo.sakhalin_payment_by_loaded_carriage,
                mo.sakhalin_payment_by_empty_carriage,
                mo.sakhalin_payment_distance,
                mo.crimea_payment_by_loaded_carriage,
                mo.crimea_payment_by_empty_carriage,
                mo.crimea_payment_distance,
                mo.kazakhstan_payment_by_loaded_carriage,
                mo.kazakhstan_payment_by_empty_carriage,
                mo.kazakhstan_payment_distance,
                mo.litva_payment_by_loaded_carriage,
                mo.litva_payment_by_empty_carriage,
                mo.litva_payment_distance,
                mo.belarus_payment_by_loaded_carriage,
                mo.belarus_payment_by_empty_carriage,
                mo.belarus_payment_distance,
                mo.zhdn_payment_by_loaded_carriage,
                mo.zhdn_payment_by_empty_carriage,
                mo.zhdn_payment_distance,
                mo.mainland_currency_of_result,
                mo.sakhalin_currency_of_result,
                mo.crimea_currency_of_result,
                mo.kazakhstan_currency_of_result,
                mo.litva_currency_of_result,
                mo.belarus_currency_of_result,
                mo.zhdn_currency_of_result,
                mo.date_calculation,
                mo.ETSNG_to_avoid,
                mo.station_otpr_name_in_system,
                mo.station_nazn_name_in_system,
                mo.station_otpr_subject_RF,
                mo.station_otpr_region,
                mo.station_otpr_polygon,
                mo.station_nazn_subject_RF,
                mo.station_nazn_region,
                mo.station_nazn_polygon,
            ]

            cursor.execute(query, values)
            connection.commit()

            # TODO: заменить запись в базу mo.date_calculation на str(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            # TODO: убрать ото всюду из выгрузок ETSNG_to_avoid, так как очистка плохих ЕСР проходит до расчетов

    except sqlite3.Error as exp:
        print("Ошибка при заполнении ячеек БД результатами расчёта:", exp)
