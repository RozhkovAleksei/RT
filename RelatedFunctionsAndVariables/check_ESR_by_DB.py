from pandas import concat
from tqdm import tqdm

# Блок для проверки кода станции ЕСР на валидность.
# Запускается отдельно, но можно интегрировать первым шагом, чтобы остановить выполнения расчётов, либо исключить
# корреспонденции, по которым есть проблема с валидностью ЕСР (отправление / назначение).
# Проверка выполняется путём поиска станции в списке stations_set, который выгружен из БД.

# Сделано, но пока не используется, для будущих доработок.
# При автоматизации получения данных с сервера - целесообразно дописать и использовать вместо RT

# def RunCheck(dataframe, stations_set):
#
#     # Создается датафрейм с выделенными столбцами из исходного файла.
#     df_1 = dataframe[['esr_otpr', 'year_for_tariff', 'month_for_tariff', 'day_for_tariff']]
#     # Создается датафрейм с выделенными столбцами из исходного файла. Столбцы с датой также нужны для объединения.
#     df_2 = dataframe[['esr_nazn', 'year_for_tariff', 'month_for_tariff', 'day_for_tariff']]
#     # Переименовывается название столбца, чтобы при объединении данные слились в один столбец.
#     df_2 = df_2.rename(columns={'esr_nazn': 'esr_otpr'})
#     # Объединение данных в один столбец.
#     df_3 = concat([df_1, df_2], ignore_index=True, axis=0)
#     # Убираются полные дубликаты полученных строк, по которым совпадает и ЕСР и дата расчёта.
#     df_3 = df_3.drop_duplicates(ignore_index=True)
#     print("Количество уникальных ЕСР: ", df_3.shape[0])
#
#     problem_ESR = {}
#
#     tmp_set_1=set()
#     tmp_set_2=set()
#
#     if len(stations_set) > 0:
#         for j in tqdm(range(0, df_3.shape[0])):
#             for k in stations_set:
#                 tmp_set_2.add(df_3['esr_otpr'][j][:-1])
#                 if df_3['esr_otpr'][j][:-1] == str(k[0]):
#                     # print("нашлось в выгрузке", k[0], k[1], k[2], k[3], k[4])
#                     tmp_set_1.add(str(k[0]))
#                 else:
#                     # problem_ESR[df_3['ЕСР Станция отправления'][j]] = df_3['Год расчета'][j]
#                     pass
#
#     print(tmp_set_2.difference(tmp_set_1))
