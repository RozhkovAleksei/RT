from time import sleep, perf_counter
from pyautogui import press, click
import corr_object_related_functions as corf
from externals import db_filename, table_name, sleep_long, sleep_short, sleep_tic
from loguru import logger

import s0_StartNewCalc as S0nc
import s1_SetBeginEndStations as S1sbes
import s2_SetTypeOfDispatch as S2std
import s3_SetMassAndETSNG as S3sme
import s4_SetCarriageSpecs as S4scs
import s5_SetCarriageReturnOptions as S5sr
import s6_GetResultsToClipboard as S6rtc
import s7_ExportResultsToExcel as S7rte
import s8_ExportDetailsToExcel as S8rte
import s9_ExportResultsToDB as S9rtdb


@logger.catch(reraise=True)
def run(source_file, details_folder, sheet_name, df, stations_meta_data):

    # Запуск цикла, в рамках которого будет построчно считываться информация из датафрейма.
    for cur_row in range(len(df)):

        # В каждой итерации пересоздаётся объект с дефолтными параметрами (защита от результатов предыдущего расчёта).
        CurCorr = corf.OneCorr()

        # Начало замера времени итерации
        start_t = perf_counter()

        # Инициализируются поля объекта данными из датафрейма
        corf.fill_object(CurCorr, df, cur_row)

        # try-except сделан, чтобы какая-то проблема не останавливала цикл
        try:

            # Вызов функций из модулей, соответствующих этапам заполнения данных для расчета в RT.
            # Везде по коду - установлена задержка для отработки непосредственно самого окна интерфейса программы RT.
            # В зависимости от скорости отработки окна интерфейса - установлены long, short задержки, они определены
            # опытным путём, поэтому в целях перестраховки ставится задержка с запасом.

            S0nc.set_new_calculation(CurCorr)

            sleep(sleep_long)

            S1sbes.set_begin_end_stations(CurCorr)

            sleep(sleep_short)

            S2std.set_type_of_dispatch(CurCorr)

            sleep(sleep_short)

            S3sme.set_etsng_and_mass_in_car(CurCorr)

            sleep(sleep_short)

            S4scs.set_car_type_capacity_amount_in_group(CurCorr)

            sleep(sleep_short)

            S5sr.set_car_return_option()

            sleep(sleep_short)

            S6rtc.get_results_to_clipboard_and_fill_object(CurCorr)

            # Добавление дополнительных данных о станциях в поля объекта для унификации выгрузки в Excel и ДБ
            corf.fill_additional_stations_data_to_object(CurCorr, stations_meta_data)

            sleep(sleep_short)

            S7rte.export_results_source_excel(df, cur_row, CurCorr, sheet_name, source_file)

            sleep(sleep_short)

            S8rte.export_details_to_new_excels(details_folder, CurCorr)

            sleep(sleep_tic)

            # Инфо-вывод текущей корреспонденции
            corf.cur_state_print(cur_row, df, CurCorr)

            # Запись текущей корреспонденции с результатами расчета в БД
            S9rtdb.write_corr_result_to_db(CurCorr, db_filename, table_name)

            sleep(sleep_short)

            # Удаляется объект. Нужно, чтобы гарантированно избежать данных с предыдущей итерации.
            del CurCorr

            # Окончание замера времени.
            end_t = perf_counter()
            print('Done in', int(end_t - start_t), 'sec.')

        except Exception as exc:
            print(exc)
            sleep(sleep_long)
            click()
            press('esc')
            press('esc')
            continue
