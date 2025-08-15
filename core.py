"""Этот модуль запускает основное ядро расчётов, которое поочередно вызывает функции взаимодействия с RT."""

import asyncio
from time import perf_counter, sleep

from loguru import logger
from pyautogui import click, press

from related_funcs_and_variables import corr_object_related_functions as corf
from related_funcs_and_variables import get_stations_data_by_DB as gsdb
from related_funcs_and_variables.externals import (
    db_filename,
    sleep_long,
    sleep_short,
    sleep_tic,
    table_name,
)

from related_funcs_and_variables.get_etran_data import send_xml_post_request

from steps_rt import s0_start_new_calc as S0nc
from steps_rt import s1_set_begin_end_stations as S1sbes
from steps_rt import s2_set_type_of_dispatch as S2std
from steps_rt import s3_set_mass_and_etsng as S3sme
from steps_rt import s4_set_carriage_specs as S4scs
from steps_rt import s5_set_carriage_return_options as S5sr
from steps_rt import s6_get_results_to_clipboard as S6rtc
from steps_rt import s7_export_results_to_excel as S7rte
from steps_rt import s8_export_details_to_excels as S8rte
from steps_rt import s9_export_results_to_db as S9rtdb


@logger.catch(reraise=True)
async def run(source_file, details_folder, sheet_name, df):

    # Подтягивается из БД дополнительная информация о станциях отправления/назначения, хранится в массиве данных
    task_get_data_from_server = asyncio.create_task(
        gsdb.get_additional_data_about_stations(df)
    )
    # Передача управления event loop
    await asyncio.sleep(0)

    # Запуск цикла, в рамках которого будет построчно считываться информация из датафрейма.
    for cur_row in range(len(df)):

        # Начало замера времени итерации
        start_t = perf_counter()

        # В каждой итерации пересоздаётся объект с дефолтными параметрами (защита от результатов предыдущего расчёта).
        CurCorr = corf.OneCorr()

        # Инициализируются поля объекта данными из датафрейма
        corf.fill_object(CurCorr, df, cur_row)

        # Инфо-вывод текущей корреспонденции
        corf.cur_state_print(cur_row, df, CurCorr)

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
            sleep(sleep_short)

            # Добавление дополнительных данных о станциях в поля объекта для унификации выгрузки в Excel и ДБ
            stations_meta_data = await task_get_data_from_server
            corf.fill_additional_stations_data_to_object(CurCorr, stations_meta_data)

            task_write_res_excel = asyncio.create_task(
                S7rte.export_results_source_excel(
                    df, cur_row, CurCorr, sheet_name, source_file
                )
            )
            await asyncio.sleep(0)
            sleep(sleep_short)

            task_write_dets_excel = asyncio.create_task(
                S8rte.export_details_to_new_excels(details_folder, CurCorr)
            )
            await asyncio.sleep(0)
            sleep(sleep_tic)

            # Запись текущей корреспонденции с результатами расчета в БД
            task_write_to_db = asyncio.create_task(
                S9rtdb.write_corr_result_to_db(CurCorr, db_filename, table_name)
            )
            await asyncio.sleep(0)
            sleep(sleep_short)

            # Ожидание исполнения асинхронных функций.
            # Удаляется объект. Нужно, чтобы гарантированно избежать данных с предыдущей итерации. Перестраховка.
            await task_write_res_excel
            await task_write_dets_excel
            await task_write_to_db

            # АЛЬТЕРНАТИВНЫЙ СЦЕНАРИЙ: получение данных о тарифе
            send_xml_post_request(CurCorr)

            del CurCorr

            # Окончание замера времени.
            end_t = perf_counter()
            print("Done in", int(end_t - start_t), "sec.")

        except Exception as exc:
            print(exc)
            sleep(sleep_long)
            click()
            press("esc")
            press("esc")
            continue
