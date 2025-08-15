from datetime import datetime

from loguru import logger
from pandas import ExcelWriter


@logger.catch(reraise=True)
async def export_results_source_excel(df, cur_row, mobj, sheet_name, source_file):
    # Заполнение текущей строки датафрейма результатами расчета текущей итерации.
    # cur_row номер строки в датафрейме для позиционирования в файле Excel, 16,17 и тд. - столбец в excel-файле

    df.iat[cur_row, 0] = mobj.esr_otpr
    df.iat[cur_row, 1] = mobj.station_otpr_name
    df.iat[cur_row, 2] = mobj.esr_nazn
    df.iat[cur_row, 3] = mobj.station_nazn_name
    df.iat[cur_row, 4] = mobj.type_dispatch
    df.iat[cur_row, 5] = mobj.is_container_train
    df.iat[cur_row, 6] = mobj.etsng_cargo
    df.iat[cur_row, 7] = mobj.mass_in_car
    df.iat[cur_row, 8] = mobj.type_of_container
    df.iat[cur_row, 9] = mobj.type_of_car
    df.iat[cur_row, 10] = mobj.car_dead_weight
    df.iat[cur_row, 11] = mobj.cars_amount_in_train
    df.iat[cur_row, 12] = mobj.year_for_tariff
    df.iat[cur_row, 13] = mobj.month_for_tariff
    df.iat[cur_row, 14] = mobj.day_for_tariff
    df.iat[cur_row, 15] = mobj.specific_van_for_coal_id
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
    df.iat[cur_row, 45] = mobj.ETSNG_to_avoid
    df.iat[cur_row, 46] = mobj.station_otpr_name_in_system
    df.iat[cur_row, 47] = mobj.station_otpr_subject_RF
    df.iat[cur_row, 48] = mobj.station_otpr_region
    df.iat[cur_row, 49] = mobj.station_otpr_polygon
    df.iat[cur_row, 50] = mobj.station_nazn_name_in_system
    df.iat[cur_row, 51] = mobj.station_nazn_subject_RF
    df.iat[cur_row, 52] = mobj.station_nazn_region
    df.iat[cur_row, 53] = mobj.station_nazn_polygon

    try:
        # выгрузка в Excel заполненного на данной итерации цикла датасета в папку проекта.
        with ExcelWriter(
            source_file, mode="a", engine="openpyxl", if_sheet_exists="replace"
        ) as writer:
            df.to_excel(writer, sheet_name=str(sheet_name + "_result"))
    except Exception as e:
        print(e)
        # print('Проблема записи результатов расчета в файл данных')
