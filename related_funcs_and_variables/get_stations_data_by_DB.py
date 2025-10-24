import requests
from loguru import logger
from pandas import concat
from tqdm import tqdm
from time import sleep
import sqlite3
from related_funcs_and_variables.confidentials import url_to_stations_bd
from related_funcs_and_variables.externals import stations_meta_data_db, sleep_short, sleep_long


# Блок для добавления территориальной информации про станции
# На вход приходит датафрейм с кодами ЕСР станций, на выходе список ЕСР кодов
@logger.catch(reraise=True)
# async def get_additional_data_about_stations(dataframe):
def get_additional_data_about_stations(dataframe):

    # Создается датафрейм с отдельными столбцами из исходного файла.
    # Оставляются ЕСР станции отправления и наименование станции отправления
    df_1 = dataframe[["esr_otpr", "station_otpr_name"]].copy()
    df_1.sort_values("esr_otpr", inplace=True)
    df_1.drop(columns={"station_otpr_name"}, inplace=True)
    df_1.drop_duplicates(keep="first", inplace=True)

    # Создается датафрейм с отдельными столбцами из исходного файла. Столбцы с датой также нужны для объединения.
    # Оставляются ЕСР станции назначения и наименование станции назначения
    df_2 = dataframe[["esr_nazn", "station_nazn_name"]].copy()
    df_2.sort_values("esr_nazn", inplace=True)
    df_2.drop(columns={"station_nazn_name"}, inplace=True)
    df_2.drop_duplicates(keep="first", inplace=True)

    del dataframe

    # Переименовывается название столбца, чтобы при объединении данные слились в один столбец.
    df_2.columns = ["esr_otpr"]

    # Объединение данных в один столбец.
    df_3 = concat([df_1, df_2], ignore_index=True, axis=0)

    # Сортируется новый датафрейм с ЕСР станций
    df_3.sort_values("esr_otpr", inplace=True)

    # Убираются полные дубликаты полученных строк, по которым совпадает и ЕСР и дата расчёта.
    df_3.drop_duplicates(ignore_index=True, inplace=True)

    del df_1
    del df_2

    stations_data = list()

    # Забирается информация о станциях с сетевого ресурса
    st_data = requests.get(url_to_stations_bd)

    # Если не удалось соединиться с сервером, возвращается пустой список станций (это не критичные данные)
    if st_data.status_code != 200:
        print("Проблема с соединением для получения данных!", st_data.status_code)
        return stations_data

    st_dict = st_data.json()

    # Итерируемся по значениям словаря длины 1, в котором 1 ключ 'rows', а значение - список пар 'ключ:значение',
    # внутри которого будет дальнейший поиск. Фактически в этом цикле 1 шаг.
    for v in st_dict.values():

        # Цикл с количеством итераций, равным количеству элементов в общем списке станций из данных сервера (очень много).
        # Будем бежать по всему списку станций из сервера через итератор [i].
        for i in tqdm(range(len(st_dict["rows"]))):
        # for i in range(len(st_dict['rows'])): #если не нужно видеть прогресс tqdm

            # Цикл с количеством итераций, равным количеству элементов в списке уникальных значений станций (из df_3)
            # Будем бежать по списку уникальных элементов - уникальных кодов станций, участвующих в расчёте тарифов.
            for j in range(0, df_3.shape[0]):

                # Если код ЕСР станции из df_3 равен коду станции в общем списке станций - добавляем в
                # список нужную информацию по этой станции. ЕСР без последнего знака, т.к. его на сервере нет
                if df_3.loc[j][0][:-1] == v[i]["stan_esr"]:

                    # TODO: сделать выгрузку в БД и подцепить данные из БД!
                    # with sqlite3.connect(stations_meta_data_db) as connection:
                    #     cursor = connection.cursor()
                    #     cursor.execute(
                    #         'insert into "stations_metadata" ("stan_esr", "stan_name", "subject", "okrug", "poligon_short_name") values ()'
                    #     )

                    stations_data.append(
                        [
                            v[i]["stan_esr"],
                            v[i]["stan_name"],
                            v[i]["subject"],
                            v[i]["okrug"],
                            v[i]["poligon_short_name"],
                        ]
                    )

    stations_data.sort(key=lambda x: x[0])

    del v
    del df_3
    del st_data
    del st_dict

    return stations_data
