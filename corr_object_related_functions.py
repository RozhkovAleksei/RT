from datetime import datetime
from pydantic import BaseModel, ConfigDict, StrictStr
from loguru import logger

# Класс для создания общего объекта, который хранит в себе все результаты расчётов по i-й корреспонденции.
# Класс создан для удобства обращения к полям при переходе выполнения программы из одного модуля - в другой.
# Иных целей - инкапсуляции (с целью ограничить доступ к полям), наследования, полиморфизма, абстракции не имеет.
class OneCorr(BaseModel):

    model_config = ConfigDict(validate_assignment=True)

    esr_otpr:StrictStr = ""
    station_otpr_name:StrictStr = ""
    esr_nazn:StrictStr = ""
    station_nazn_name:StrictStr = ""
    type_dispatch:StrictStr = ""
    is_container_train:StrictStr = ""
    etsng_cargo:StrictStr = ""
    mass_in_car:StrictStr = ""
    type_of_container:StrictStr = ""
    type_of_car:StrictStr = ""
    car_dead_weight:StrictStr = ""
    cars_amount_in_train:StrictStr = ""
    year_for_tariff:StrictStr = ""
    month_for_tariff:StrictStr = ""
    day_for_tariff:StrictStr = ""
    specific_van_for_coal_id: StrictStr = ' '
    mainland_payment_by_loaded_carriage:StrictStr = ""
    mainland_payment_by_empty_carriage:StrictStr = ""
    mainland_payment_distance:StrictStr = ""
    sakhalin_payment_by_loaded_carriage:StrictStr = ""
    sakhalin_payment_by_empty_carriage:StrictStr = ""
    sakhalin_payment_distance:StrictStr = ""
    crimea_payment_by_loaded_carriage:StrictStr = ""
    crimea_payment_by_empty_carriage:StrictStr = ""
    crimea_payment_distance:StrictStr = ""
    kazakhstan_payment_by_loaded_carriage:StrictStr = ""
    kazakhstan_payment_by_empty_carriage:StrictStr = ""
    kazakhstan_payment_distance:StrictStr = ""
    litva_payment_by_loaded_carriage:StrictStr = ""
    litva_payment_by_empty_carriage:StrictStr = ""
    litva_payment_distance:StrictStr = ""
    belarus_payment_by_loaded_carriage:StrictStr = ""
    belarus_payment_by_empty_carriage:StrictStr = ""
    belarus_payment_distance:StrictStr = ""
    zhdn_payment_by_loaded_carriage:StrictStr = ""
    zhdn_payment_by_empty_carriage:StrictStr = ""
    zhdn_payment_distance:StrictStr = ""
    mainland_currency_of_result:StrictStr = "RUB"
    sakhalin_currency_of_result:StrictStr = "RUB"
    crimea_currency_of_result:StrictStr = "RUB"
    kazakhstan_currency_of_result:StrictStr = "CHF"
    litva_currency_of_result:StrictStr = "CHF"
    belarus_currency_of_result:StrictStr = "CHF"
    zhdn_currency_of_result: StrictStr = "RUB"
    date_calculation: StrictStr = ""
    ETSNG_to_avoid: StrictStr = ''
    station_otpr_name_in_system:StrictStr = ''
    station_nazn_name_in_system: StrictStr = ''
    station_otpr_subject_RF:StrictStr = ''
    station_otpr_region:StrictStr = ''
    station_otpr_polygon:StrictStr = ''
    station_nazn_subject_RF:StrictStr = ''
    station_nazn_region:StrictStr = ''
    station_nazn_polygon:StrictStr = ''

    # Явное удаление объекта
    # def __del__(self):
    #     import gc
    #     gc.collect()

# Инициализация переменных значениями из текущей строки датафрейма.
# Можно вместо переменных сделать ассоциативный массив, но читаемость кода ухудшится.
# Зато было бы удобно через JSON передавать куда-то дальше.
@logger.catch(reraise=True)
def fill_object(m_obj, df, cur_row):

    m_obj.esr_otpr = df.iloc[cur_row]['esr_otpr']
    m_obj.station_otpr_name = df.iloc[cur_row]['station_otpr_name']
    m_obj.esr_nazn = df.iloc[cur_row]['esr_nazn']
    m_obj.station_nazn_name = df.iloc[cur_row]['station_nazn_name']
    m_obj.type_dispatch = df.iloc[cur_row]['type_dispatch']
    m_obj.is_container_train = df.iloc[cur_row]['is_container_train']
    m_obj.etsng_cargo = df.iloc[cur_row]['etsng_cargo']
    m_obj.mass_in_car = df.iloc[cur_row]['mass_in_car']
    m_obj.type_of_container = df.iloc[cur_row]['type_of_container']
    m_obj.type_of_car = df.iloc[cur_row]['type_of_car']
    m_obj.car_dead_weight = df.iloc[cur_row]['car_dead_weight']
    m_obj.cars_amount_in_train = df.iloc[cur_row]['cars_amount_in_train']
    m_obj.year_for_tariff = df.iloc[cur_row]['year_for_tariff']
    m_obj.month_for_tariff = df.iloc[cur_row]['month_for_tariff']
    m_obj.day_for_tariff = df.iloc[cur_row]['day_for_tariff']
    m_obj.date_calculation = m_obj.year_for_tariff + "." + m_obj.month_for_tariff + "." + m_obj.day_for_tariff
    m_obj.specific_van_for_coal_id = df.iloc[cur_row]['specific_van_for_coal_id']

# Заполнение полей объекта дополнительной информацией о станциях
@logger.catch(reraise=True)
def fill_additional_stations_data_to_object(mobj, stations_meta_data):

    for station_data in stations_meta_data:

        # Ищется сравнение по неполному коду ЕСР, так как в НСИ последний (шестой) знак кода ЕСР не используется
        if mobj.esr_otpr[:-1] == str(station_data[0]):

            mobj.station_otpr_name_in_system = station_data[1]  # Наименование станции отправления в системах
            mobj.station_otpr_subject_RF = station_data[2]  # Принадлежность станции отправления к субъекту РФ
            mobj.station_otpr_region = station_data[3]  # Принадлежность станции отправления к федеральному округу
            mobj.station_otpr_polygon = station_data[4]  # Принадлежность станции отправления к полигону

        # Ищется сравнение по неполному коду ЕСР, так как в НСИ последний (шестой) знак кода ЕСР не используется
        if mobj.esr_nazn[:-1] == str(station_data[0]):

            mobj.station_nazn_name_in_system = station_data[1]  # Наименование станции назначения в системах
            mobj.station_nazn_subject_RF = station_data[2]  # Принадлежность станции назначения к субъекту РФ
            mobj.station_nazn_region = station_data[3]  # Принадлежность станции назначения к федеральному округу
            mobj.station_nazn_polygon = station_data[4]  # Принадлежность станции назначения к полигону


# Инфо вывод текущей корреспонденции с её параметрами
@logger.catch(reraise=True)
def cur_state_print(cur_r, dataframe, mobj):

    log_data = (datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' '
                + str(cur_r + 1) + '/' + str(len(dataframe.index)) + ' ' + dataframe.iloc[cur_r]['station_otpr_name']
                + '-' + dataframe.iloc[cur_r]['station_nazn_name'] + ', ТипОтпр - '
                + dataframe.iloc[cur_r]['type_dispatch'] + ', КонтПоезд (0/1)-'
                + dataframe.iloc[cur_r]['is_container_train'] + ', ЕТСНГ-' + dataframe.iloc[cur_r]['etsng_cargo']
                + ', Масса в вагоне-' + dataframe.iloc[cur_r]['mass_in_car'] + ', ТипКонт-'
                + dataframe.iloc[cur_r]['type_of_container'] + ', РодПС-' + dataframe.iloc[cur_r]['type_of_car']
                + ', Статн.-' + dataframe.iloc[cur_r]['car_dead_weight'] + ', Кол-воВагонов-'
                + dataframe.iloc[cur_r]['cars_amount_in_train'] + ', ДатаРасчета-' + mobj.year_for_tariff
                + '-' + mobj.month_for_tariff + '-' + mobj.day_for_tariff + ', СпецПВ-'
                + dataframe.iloc[cur_r]['specific_van_for_coal_id'] + ', СтОтпр SysName-'
                + mobj.station_otpr_name_in_system + ', СтОтпр Субъект РФ-' + mobj.station_otpr_subject_RF
                + ', СтОтпр Регион-' + mobj.station_otpr_region + ', СтОтпр Полигон-' + mobj.station_otpr_polygon
                + ', СтНазн SysName-' + mobj.station_nazn_name_in_system + ', СтНазн Субъект РФ-'
                + mobj.station_nazn_subject_RF + ', СтНазн Регион-' + mobj.station_nazn_region + ', СтНазн Полигон-'
                + mobj.station_nazn_polygon)

    print(log_data, sep=', ')

