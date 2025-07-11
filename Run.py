from time import sleep, perf_counter
from datetime import datetime
from pyautogui import press, click
import s0_StartNewCalc as S0nc
import s1_SetBeginEndStations as S1sbes
import s2_SetTypeOfDispatch as S2std
import s3_SetMassAndETSNG as S3sme
import s4_SetCarriageSpecs as S4scs
import s5_SetCarriageReturnOptions as S5sr
import s6_GetResultsToClipboard as S6rtc
import s7_ExportDetailsToExcel as S7rte
import s8_ExportResultsToDB as S8rtdb
import globals


def Run(source_file, details_folder, sheet_name, df, stations_meta_data, bad_esr):

    # На основе вычищенного датафрейма - собираем в список оставшиеся после удаления дублей индексы, по которым будет расчёт
    indexes_for_iterate = df.index.tolist()

    # Запуск цикла, в рамках которого будет построчно считываться информация из датафрейма.
    # Соответствующими данными датафрейма будут инициализированы переменные.
    # for cur_row in range(start_pos, end_pos_excluding):
    for cur_row in indexes_for_iterate:

        if (df.iloc[cur_row]['esr_otpr'] in bad_esr)

        # # Если по результатам отработки блока проверки корректности данных ЕСР есть какие-то проблемные,
        # # то они пропускаются в расчёте (проверяется наличие ключа и определённого значения среди всех значений).
        # if ((df.iloc[cur_row]['esr_otpr'] in ESR_to_exclude.keys() and df.iloc[cur_row]['year_for_tariff'] in ESR_to_exclude[df.iloc[cur_row]['esr_otpr']]) or (df.iloc[cur_row]['esr_nazn'] in ESR_to_exclude.keys() and df.iloc[cur_row]['year_for_tariff'] in ESR_to_exclude[df.iloc[cur_row]['esr_nazn']])):
        #     continue

        # В каждой итерации пересоздаётся объект с дефолтными параметрами (защита от результатов предыдущего расчёта).
        # Это порождает предупреждения о возможности обращения к переменной, которая ещё не создана далее по коду.
        mo = globals.my_obj()

        # В зависимости от компьютера, на котором проверяется код - выбирается метка диска, где лежит файл excel.
        mo.path_to_img_data = globals.SetPathToImgByScreenRes()

        try:
            # начало замера времени итерации
            start_t = perf_counter()

            # Инициализация переменных значениями из текущей строки датафрейма.
            # Можно вместо переменных сделать ассоциативный массив, но читаемость кода ухудшится.
            # Зато было бы удобно через JSON передавать куда-то дальше.
            begin_station = (df.iloc[cur_row]['esr_otpr'])
            end_station = (df.iloc[cur_row]['esr_nazn'])
            type_dispatch = df.iloc[cur_row]['type_dispatch']
            mo.is_full_train_containers = int(df.iloc[cur_row]['is_container_train'])
            ETSNG_code = str(df.iloc[cur_row]['etsng_cargo'])

            # mass_in_carriage = (df.iloc[cur_row]['Масса груза в вагоне, тонн']).replace(',', '.')
            mass_in_carriage = df.iloc[cur_row]['mass_in_car']

            container_type = df.iloc[cur_row]['type_of_container']
            carriage_type = df.iloc[cur_row]['type_of_car']

            # carriage_capacity = (df.iloc[cur_row]['Грузоподъемность']).replace(',', '.')
            carriage_capacity = df.iloc[cur_row]['car_dead_weight']

            amount_in_group = str(df.iloc[cur_row]['cars_amount_in_train'])

            # Проверка на отсутствие незаполненных данных о дате расчёта. При наличии пустых - подставляется текущая.
            if str(df.iloc[cur_row]['year_for_tariff']) != 'не указан':
                mo.calc_year = str(df.iloc[cur_row]['year_for_tariff'])
                mo.calc_month = str(df.iloc[cur_row]['month_for_tariff'])
                mo.calc_day = str(df.iloc[cur_row]['day_for_tariff'])
            else:
                mo.calc_year = str(datetime.now().strftime("%Y"))
                mo.calc_month = str(datetime.now().strftime("%m"))
                mo.calc_day = str(datetime.now().strftime("%d"))
            mo.date_calculation = mo.calc_year + "." + mo.calc_month + "." + mo.calc_day

            # Указывается специальный тип полувагона для угля (инновационный полувагон)
            mo.specific_van_for_coal_id = str(df.iloc[cur_row]['special_car_type'])

            # Инфо-вывод текущей корреспонденции
            globals.cur_state_print(cur_row, df, mo)

            # ОСНОВНОЙ ФУНКЦИОНАЛ ВЗАИМОДЕЙСТВИЯ С RT НАЧИНАЕТСЯ ЗДЕСЬ
            # Вызов функций из модулей, соответствующих этапам заполнения данных для расчета в RT.
            S0nc.SetNewCalculation(mo)

            # Везде по коду - установлена задержка для отработки непосредственно самого окна интерфейса программы RT.
            # В зависимости от скорости отработки окна интерфейса - установлены long, short задержки, определены
            # опытным путём, поэтому перестраховываемся и ставим задержку с запасом.
            sleep(mo.global_sleep_long)
            S1sbes.SetBeginEndStation(str(begin_station), str(end_station), mo)

            sleep(mo.global_sleep_short)
            S2std.SetTypeOfDispatch(type_dispatch, mo)

            sleep(mo.global_sleep_short)
            S3sme.SetETSNGCodeAndMassInCarriage(ETSNG_code, mass_in_carriage, mo)

            sleep(mo.global_sleep_short)
            S4scs.SetCarriageTypeCapacityAmountInGroup(carriage_type, container_type, carriage_capacity,
                                                       amount_in_group, type_dispatch, mo)
            sleep(mo.global_sleep_short)
            S5sr.SetReturn(mo)
            sleep(mo.global_sleep_short)
            S6rtc.GetResultsToClipboard(mo)
            sleep(mo.global_sleep_short)
            S7rte.GetDetailsFromRTarif(cur_row, details_folder)
            sleep(0.1)
            # ОСНОВНОЙ ФУНКЦИОНАЛ ВЗАИМОДЕЙСТВИЯ С RT ЗАКАНЧИВАЕТСЯ ЗДЕСЬ

            # Добавление дополнительных данных о станциях в поля объекта для унификации выгрузки в Excel и ДБ
            globals.setStationsMetaDataToObject(mo, stations_meta_data, begin_station, end_station)

            # ВЫЗОВ ФУНКЦИИ, ЗАПИСЫВАЮЩЕЙ В БД ИНФУ
            S8rtdb.write_results_to_db(cur_row, mo, stations_meta_data, begin_station, end_station)

            # Заполнение текущей строки датафрейма результатами расчета текущей итерации.
            globals.write_results_excel(df, cur_row, mo, sheet_name, source_file)

            sleep(mo.global_sleep_short)

            # Удаляется объект (очищаются поля). Нужно, чтобы избежать данных с предыдущей итерации.
            del mo

            # Окончание замера времени.
            end_t = perf_counter()
            print('Done in', int(end_t - start_t), 'sec.')

        except Exception as exc:
            print(exc)
            sleep(mo.global_sleep_long)
            click()
            press('esc')
            press('esc')
            continue
