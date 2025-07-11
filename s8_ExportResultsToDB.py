import sqlite3
from externals import table_name, db_filename

def write_results_to_db(cur_row, mo, stations_meta_data, begin_station, end_station):
    # 'UPDATE ' +'"'+table_name+'"'+ ' SET ' + a + ' = ' + aaa + ' WHERE ' + b + '=' + str(c))
    # UPDATE table_name SET "mainland_payment_by_loaded_carriage" = "str(mo.mainland_payment_by_loaded_carriage)" WHERE "index" = str(cur_row)
    # connection.cursor().execute('UPDATE '+'"'+table_name+'"' + ' SET '+'"mainland_payment_by_loaded_carriage"' + ' = ' + '"'+str(mo.mainland_payment_by_loaded_carriage)+'"', '"mainland_payment_by_empty_carriage"' + ' = ' + '"'+str(mo.mainland_payment_by_empty_carriage)+'"' + ' WHERE "index" = ' + '"'+str(cur_row)+'"')
    # CURRENT_TIMESTAMP будет ставить время GMT
    try:
        with sqlite3.connect(db_filename) as connection:

            # Проверка подключения к базе данных
            if connection is None:
                raise ConnectionError("Проблема с подключением к базе данных")

            connection.cursor().execute('UPDATE '+'"'+table_name+'"'
                                        + ' SET '
                                        +'"mainland_payment_by_loaded_carriage"' + ' = ' + '"'+str(mo.mainland_payment_by_loaded_carriage)+'"' + ','
                                        +'"mainland_payment_by_empty_carriage"' + ' = ' + '"'+str(mo.mainland_payment_by_empty_carriage)+'"' + ','
                                        +'"mainland_payment_distance"' + ' = ' + '"'+str(mo.mainland_payment_distance)+'"' + ','
                                        +'"sakhalin_payment_by_loaded_carriage"' + ' = ' + '"'+str(mo.sakhalin_payment_by_loaded_carriage)+'"' + ','
                                        +'"sakhalin_payment_by_empty_carriage"' + ' = ' + '"'+str(mo.sakhalin_payment_by_empty_carriage)+'"' + ','
                                        +'"sakhalin_payment_distance"' + ' = ' + '"'+str(mo.sakhalin_payment_distance)+'"' + ','
                                        +'"crimea_payment_by_loaded_carriage"' + ' = ' + '"'+str(mo.crimea_payment_by_loaded_carriage)+'"' + ','
                                        +'"crimea_payment_by_empty_carriage"' + ' = ' + '"'+str(mo.crimea_payment_by_empty_carriage)+'"' + ','
                                        +'"crimea_payment_distance"' + ' = ' + '"'+str(mo.crimea_payment_distance)+'"' + ','
                                        +'"kazakhstan_payment_by_loaded_carriage"' + ' = ' + '"'+str(mo.kazakhstan_payment_by_loaded_carriage)+'"' + ','
                                        +'"kazakhstan_payment_by_empty_carriage"' + ' = ' + '"'+str(mo.kazakhstan_payment_by_empty_carriage)+'"' + ','
                                        +'"kazakhstan_payment_distance"' + ' = ' + '"'+str(mo.kazakhstan_payment_distance)+'"' + ','
                                        +'"litva_payment_by_loaded_carriage"' + ' = ' + '"'+str(mo.litva_payment_by_loaded_carriage)+'"' + ','
                                        +'"litva_payment_by_empty_carriage"' + ' = ' + '"'+str(mo.litva_payment_by_empty_carriage)+'"' + ','
                                        +'"litva_payment_distance"' + ' = ' + '"'+str(mo.litva_payment_distance)+'"' + ','
                                        +'"belarus_payment_by_loaded_carriage"' + ' = ' + '"'+str(mo.belarus_payment_by_loaded_carriage)+'"' + ','
                                        +'"belarus_payment_by_empty_carriage"' + ' = ' + '"'+str(mo.belarus_payment_by_empty_carriage) + '"' + ','
                                        +'"belarus_payment_distance"' + ' = ' + '"'+str(mo.belarus_payment_distance) + '"' + ','
                                        +'"zhdn_payment_by_loaded_carriage"' + ' = ' + '"'+str(mo.zhdn_payment_by_loaded_carriage) + '"' + ','
                                        +'"zhdn_payment_by_empty_carriage"' + ' = ' + '"'+str(mo.zhdn_payment_by_empty_carriage) + '"' + ','
                                        +'"zhdn_payment_distance"' + ' = ' + '"'+str(mo.zhdn_payment_distance) + '"' + ','
                                        +'"mainland_currency_of_result"' + ' = ' + '"'+str(mo.mainland_currency_of_result) + '"' + ','
                                        +'"sakhalin_currency_of_result"' + ' = ' + '"'+str(mo.sakhalin_currency_of_result) + '"' + ','
                                        +'"crimea_currency_of_result"' + ' = ' + '"'+str(mo.crimea_currency_of_result) + '"' + ','
                                        +'"kazakhstan_currency_of_result"' + ' = ' + '"'+str(mo.kazakhstan_currency_of_result) + '"' + ','
                                        +'"litva_currency_of_result"' + ' = ' + '"'+str(mo.litva_currency_of_result) + '"' + ','
                                        +'"belarus_currency_of_result"' + ' = ' + '"'+str(mo.belarus_currency_of_result) + '"' + ','
                                        +'"zhdn_currency_of_result"' + ' = ' + '"'+str(mo.zhdn_currency_of_result) + '"' + ','
                                        +'"date_of_calc"' + ' = ' + 'CURRENT_TIMESTAMP' + ','
                                        +'"ETSNG_to_avoid"' + ' = ' + '"'+str(mo.ETSNG_to_avoid) + '"' + ','
                                        +'"station_otpr_name_in_system"' + ' = ' + '"'+str(mo.station_otpr_name_in_system) + '"' + ','
                                        +'"station_otpr_subject_RF"' + ' = ' + '"'+str(mo.station_otpr_subject_RF) + '"' + ','
                                        +'"station_otpr_region"' + ' = ' + '"'+str(mo.station_otpr_region) + '"' + ','
                                        +'"station_otpr_polygon"' + ' = ' + '"'+str(mo.station_otpr_polygon) + '"' + ','
                                        +'"station_nazn_name_in_system"' + ' = ' + '"'+str(mo.station_nazn_name_in_system) + '"' + ','
                                        +'"station_nazn_subject_RF"' + ' = ' + '"'+str(mo.station_nazn_subject_RF) + '"' + ','
                                        +'"station_nazn_region"' + ' = ' + '"'+str(mo.station_nazn_region) + '"' + ','
                                        +'"station_nazn_polygon"' + ' = ' + '"'+str(mo.station_nazn_polygon) + '"'
                                        +' WHERE "index" = ' + '"'+str(cur_row)+'"')
            connection.commit()
    except sqlite3.Error as exp:
        print("Ошибка при заполнении ячеек БД:", exp)
