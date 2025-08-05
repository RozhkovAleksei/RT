from fastapi import FastAPI, Depends, HTTPException, Query
from SQLFunctions.sql_alchemy_funcs import my_session_fabric, Corr
from typing import List
from sqlalchemy.orm import Session
from corr_object_related_functions import OneCorr

# python -m uvicorn fast_api_funcs:app --reload --host 127.0.0.1 --port 8889

app = FastAPI()

def get_db():
    with my_session_fabric() as connect_to_db:
        return connect_to_db

# Учитывая, что далее сделаны два гибких фильтра - нижеследующие запросы становятся не актуальны, но пусть будут.
# /all оставлено для теста, что работает
@app.get("/all", response_model=List[OneCorr])
def get_all(connect_to_db: Session = Depends(get_db)):

    result = connect_to_db.query(Corr).all()
    if result is None:
        raise HTTPException(404, 'corr not found')

    return result
#
# @app.get("/corr_id/{corr_id}", response_model=List[OneCorr])
# def get_corr_by_id(corr_id: int, connect_to_db: Session = Depends(get_db)):
#
#     result = connect_to_db.query(Corr)
#
#     result = result.filter(Corr.id == corr_id).all()
#
#     if result is None:
#         raise HTTPException(404, 'corr with id not found')
#     return result
#
# @app.get("/corr_esr_otpr/{esr_otpr}", response_model=List[OneCorr])
# def get_corr_by_esr_otpr(esr_otpr: str, connect_to_db: Session = Depends(get_db)):
#     result = connect_to_db.query(Corr).filter(Corr.esr_otpr == esr_otpr).all()
#     if result is None:
#         raise HTTPException(404, 'corr with esr_otpr not found')
#     return result
#
# @app.get("/corr_esr_nazn/{esr_nazn}", response_model=List[OneCorr])
# def get_corr_by_esr_nazn(esr_nazn: str, connect_to_db: Session = Depends(get_db)):
#
#     result = connect_to_db.query(Corr)
#
#     result = result.filter(Corr.esr_nazn == esr_nazn).all()
#
#     if result is None:
#         raise HTTPException(404, 'corr with esr_nazn not found')
#     return result
#
# @app.get("/corr_etsng/{etsng}", response_model=List[OneCorr])
# def get_corr_by_etsng(etsng: str, connect_to_db: Session = Depends(get_db)):
#
#     result = connect_to_db.query(Corr)
#
#     result = result.filter(Corr.etsng_cargo == etsng).all()
#     if result is None:
#         raise HTTPException(404, 'corr with etsng not found')
#     return result
#
# @app.get("/type_dispatch/{type_disp}", response_model=List[OneCorr])
# def get_corr_by_type_dispatch(type_disp: str, connect_to_db: Session = Depends(get_db)):
#
#     result = connect_to_db.query(Corr)
#
#     result = result.filter(Corr.type_dispatch == type_disp).all()
#
#     if result is None:
#         raise HTTPException(404, 'corr with type dispatch not found')
#
#     return result
#
# @app.get("/type_car/{type_car}", response_model=List[OneCorr])
# def get_corr_by_type_car(type_car: str, connect_to_db: Session = Depends(get_db)):
#
#     result = connect_to_db.query(Corr)
#
#     result = result.filter(Corr.type_of_car == type_car).all()
#
#     if result is None:
#         raise HTTPException(404, 'corr with type car not found')
#     return result

@app.get("/search", response_model=List[OneCorr])
def get_corr_by_filter(
        esr_otpr: str = Query(None, description="Код станции отправления (ЕСР)"),
        station_otpr_name: str = Query(None, description="Название станции отправления"),
        esr_nazn: str = Query(None, description="Код станции назначения (ЕСР)"),
        station_nazn_name: str = Query(None, description="Название станции назначения"),
        type_dispatch: str = Query(None, description="Тип отправки"),
        is_container_train: str = Query(None, description="Признак контейнерного поезда (1/0)"),
        etsng_cargo: str = Query(None, description="Код груза по ЕТСНГ"),
        mass_in_car: str = Query(None, description="Масса в вагоне"),
        type_of_container: str = Query(None, description="Тип контейнера"),
        type_of_car: str = Query(None, description="Тип вагона"),
        car_dead_weight: str = Query(None, description="Грузоподъемность вагона"),
        cars_amount_in_train: str = Query(None, description="Количество вагонов в поезде"),
        year_for_tariff: str = Query(None, description="Год расчёта тарифа"),
        month_for_tariff: str = Query(None, description="Месяц расчёта тарифа"),
        day_for_tariff: str = Query(None, description="День расчёта тарифа"),
        specific_van_for_coal_id: str = Query(None, description="Идентификатор специального вагона для угля"),
        mainland_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (материк)"),
        sakhalin_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Сахалин)"),
        crimea_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Крым)"),
        kazakhstan_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Казахстан)"),
        litva_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Литва)"),
        belarus_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Беларусь)"),
        zhdn_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (ЖДН)"),
        mainland_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (материк)"),
        sakhalin_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Сахалин)"),
        crimea_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Крым)"),
        kazakhstan_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Казахстан)"),
        litva_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Литва)"),
        belarus_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Беларусь)"),
        zhdn_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (ЖДН)"),
        mainland_payment_distance: str = Query(None, description="Тарифное расстояние (материк)"),
        sakhalin_payment_distance: str = Query(None, description="Тарифное расстояние (Сахалин)"),
        crimea_payment_distance: str = Query(None, description="Тарифное расстояние (Крым)"),
        kazakhstan_payment_distance: str = Query(None, description="Тарифное расстояние (Казахстан)"),
        litva_payment_distance: str = Query(None, description="Тарифное расстояние (Литва)"),
        belarus_payment_distance: str = Query(None, description="Тарифное расстояние (Беларусь)"),
        zhdn_payment_distance: str = Query(None, description="Тарифное расстояние (ЖДН)"),
        mainland_currency_of_result: str = Query(None, description="Валюта результата (материк)"),
        sakhalin_currency_of_result: str = Query(None, description="Валюта результата (Сахалин)"),
        crimea_currency_of_result: str = Query(None, description="Валюта результата (Крым)"),
        kazakhstan_currency_of_result: str = Query(None, description="Валюта результата (Казахстан)"),
        litva_currency_of_result: str = Query(None, description="Валюта результата (Литва)"),
        belarus_currency_of_result: str = Query(None, description="Валюта результата (Беларусь)"),
        zhdn_currency_of_result: str = Query(None, description="Валюта результата (ЖДН)"),
        date_calculation: str = Query(None, description="Дата расчёта"),
        ETSNG_to_avoid: str = Query(None, description="ЕТСНГ для исключения"),
        station_otpr_name_in_system: str = Query(None, description="Название станции отправления в системе"),
        station_nazn_name_in_system: str = Query(None, description="Название станции назначения в системе"),
        station_otpr_subject_RF: str = Query(None, description="Субъект РФ станции отправления"),
        station_otpr_region: str = Query(None, description="Регион станции отправления"),
        station_otpr_polygon: str = Query(None, description="Полигон станции отправления"),
        station_nazn_subject_RF: str = Query(None, description="Субъект РФ станции назначения"),
        station_nazn_region: str = Query(None, description="Регион станции назначения"),
        station_nazn_polygon: str = Query(None, description="Полигон станции назначения"),
        connect_to_db: Session = Depends(get_db)
):
    filters = {
        "esr_otpr": esr_otpr,
        "station_otpr_name": station_otpr_name,
        "esr_nazn": esr_nazn,
        "station_nazn_name": station_nazn_name,
        "type_dispatch": type_dispatch,
        "is_container_train": is_container_train,
        "etsng_cargo": etsng_cargo,
        "mass_in_car": mass_in_car,
        "type_of_container": type_of_container,
        "type_of_car": type_of_car,
        "car_dead_weight": car_dead_weight,
        "cars_amount_in_train": cars_amount_in_train,
        "year_for_tariff": year_for_tariff,
        "month_for_tariff": month_for_tariff,
        "day_for_tariff": day_for_tariff,
        "specific_van_for_coal_id": specific_van_for_coal_id,
        "mainland_payment_by_loaded_carriage": mainland_payment_by_loaded_carriage,
        "sakhalin_payment_by_loaded_carriage": sakhalin_payment_by_loaded_carriage,
        "crimea_payment_by_loaded_carriage": crimea_payment_by_loaded_carriage,
        "kazakhstan_payment_by_loaded_carriage": kazakhstan_payment_by_loaded_carriage,
        "litva_payment_by_loaded_carriage": litva_payment_by_loaded_carriage,
        "belarus_payment_by_loaded_carriage": belarus_payment_by_loaded_carriage,
        "zhdn_payment_by_loaded_carriage": zhdn_payment_by_loaded_carriage,
        "mainland_payment_by_empty_carriage": mainland_payment_by_empty_carriage,
        "sakhalin_payment_by_empty_carriage": sakhalin_payment_by_empty_carriage,
        "crimea_payment_by_empty_carriage": crimea_payment_by_empty_carriage,
        "kazakhstan_payment_by_empty_carriage": kazakhstan_payment_by_empty_carriage,
        "litva_payment_by_empty_carriage": litva_payment_by_empty_carriage,
        "belarus_payment_by_empty_carriage": belarus_payment_by_empty_carriage,
        "zhdn_payment_by_empty_carriage": zhdn_payment_by_empty_carriage,
        "mainland_payment_distance": mainland_payment_distance,
        "sakhalin_payment_distance": sakhalin_payment_distance,
        "crimea_payment_distance": crimea_payment_distance,
        "kazakhstan_payment_distance": kazakhstan_payment_distance,
        "litva_payment_distance": litva_payment_distance,
        "belarus_payment_distance": belarus_payment_distance,
        "zhdn_payment_distance": zhdn_payment_distance,
        "mainland_currency_of_result": mainland_currency_of_result,
        "sakhalin_currency_of_result": sakhalin_currency_of_result,
        "crimea_currency_of_result": crimea_currency_of_result,
        "kazakhstan_currency_of_result": kazakhstan_currency_of_result,
        "litva_currency_of_result": litva_currency_of_result,
        "belarus_currency_of_result": belarus_currency_of_result,
        "zhdn_currency_of_result": zhdn_currency_of_result,
        "date_calculation": date_calculation,
        "ETSNG_to_avoid": ETSNG_to_avoid,
        "station_otpr_name_in_system": station_otpr_name_in_system,
        "station_nazn_name_in_system": station_nazn_name_in_system,
        "station_otpr_subject_RF": station_otpr_subject_RF,
        "station_otpr_region": station_otpr_region,
        "station_otpr_polygon": station_otpr_polygon,
        "station_nazn_subject_RF": station_nazn_subject_RF,
        "station_nazn_region": station_nazn_region,
        "station_nazn_polygon": station_nazn_polygon,
    }

    result = connect_to_db.query(Corr)

    for attr, value in filters.items():
        if value is not None:
            result = result.filter(getattr(Corr, attr) == value)

    # Например
    # http://localhost:8889/search?station_otpr_region=Уральский&year_for_tariff=2022

    return result.all()

@app.get("/unique_values/{field}", response_model=List[str])
def get_uniq_values_by_filter(
        field: str,
        esr_otpr: str = Query(None, description="Код станции отправления (ЕСР)"),
        station_otpr_name: str = Query(None, description="Название станции отправления"),
        esr_nazn: str = Query(None, description="Код станции назначения (ЕСР)"),
        station_nazn_name: str = Query(None, description="Название станции назначения"),
        type_dispatch: str = Query(None, description="Тип отправки"),
        is_container_train: str = Query(None, description="Признак контейнерного поезда (1/0)"),
        etsng_cargo: str = Query(None, description="Код груза по ЕТСНГ"),
        mass_in_car: str = Query(None, description="Масса в вагоне"),
        type_of_container: str = Query(None, description="Тип контейнера"),
        type_of_car: str = Query(None, description="Тип вагона"),
        car_dead_weight: str = Query(None, description="Грузоподъемность вагона"),
        cars_amount_in_train: str = Query(None, description="Количество вагонов в поезде"),
        year_for_tariff: str = Query(None, description="Год расчёта тарифа"),
        month_for_tariff: str = Query(None, description="Месяц расчёта тарифа"),
        day_for_tariff: str = Query(None, description="День расчёта тарифа"),
        specific_van_for_coal_id: str = Query(None, description="Идентификатор специального вагона для угля"),
        mainland_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (материк)"),
        sakhalin_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Сахалин)"),
        crimea_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Крым)"),
        kazakhstan_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Казахстан)"),
        litva_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Литва)"),
        belarus_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (Беларусь)"),
        zhdn_payment_by_loaded_carriage: str = Query(None, description="Тариф за груженый вагон (ЖДН)"),
        mainland_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (материк)"),
        sakhalin_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Сахалин)"),
        crimea_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Крым)"),
        kazakhstan_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Казахстан)"),
        litva_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Литва)"),
        belarus_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (Беларусь)"),
        zhdn_payment_by_empty_carriage: str = Query(None, description="Тариф за порожний вагон (ЖДН)"),
        mainland_payment_distance: str = Query(None, description="Тарифное расстояние (материк)"),
        sakhalin_payment_distance: str = Query(None, description="Тарифное расстояние (Сахалин)"),
        crimea_payment_distance: str = Query(None, description="Тарифное расстояние (Крым)"),
        kazakhstan_payment_distance: str = Query(None, description="Тарифное расстояние (Казахстан)"),
        litva_payment_distance: str = Query(None, description="Тарифное расстояние (Литва)"),
        belarus_payment_distance: str = Query(None, description="Тарифное расстояние (Беларусь)"),
        zhdn_payment_distance: str = Query(None, description="Тарифное расстояние (ЖДН)"),
        mainland_currency_of_result: str = Query(None, description="Валюта результата (материк)"),
        sakhalin_currency_of_result: str = Query(None, description="Валюта результата (Сахалин)"),
        crimea_currency_of_result: str = Query(None, description="Валюта результата (Крым)"),
        kazakhstan_currency_of_result: str = Query(None, description="Валюта результата (Казахстан)"),
        litva_currency_of_result: str = Query(None, description="Валюта результата (Литва)"),
        belarus_currency_of_result: str = Query(None, description="Валюта результата (Беларусь)"),
        zhdn_currency_of_result: str = Query(None, description="Валюта результата (ЖДН)"),
        date_calculation: str = Query(None, description="Дата расчёта"),
        ETSNG_to_avoid: str = Query(None, description="ЕТСНГ для исключения"),
        station_otpr_name_in_system: str = Query(None, description="Название станции отправления в системе"),
        station_nazn_name_in_system: str = Query(None, description="Название станции назначения в системе"),
        station_otpr_subject_RF: str = Query(None, description="Субъект РФ станции отправления"),
        station_otpr_region: str = Query(None, description="Регион станции отправления"),
        station_otpr_polygon: str = Query(None, description="Полигон станции отправления"),
        station_nazn_subject_RF: str = Query(None, description="Субъект РФ станции назначения"),
        station_nazn_region: str = Query(None, description="Регион станции назначения"),
        station_nazn_polygon: str = Query(None, description="Полигон станции назначения"),
        connect_to_db: Session = Depends(get_db)
):

    filters = {
        "esr_otpr": esr_otpr,
        "station_otpr_name": station_otpr_name,
        "esr_nazn": esr_nazn,
        "station_nazn_name": station_nazn_name,
        "type_dispatch": type_dispatch,
        "is_container_train": is_container_train,
        "etsng_cargo": etsng_cargo,
        "mass_in_car": mass_in_car,
        "type_of_container": type_of_container,
        "type_of_car": type_of_car,
        "car_dead_weight": car_dead_weight,
        "cars_amount_in_train": cars_amount_in_train,
        "year_for_tariff": year_for_tariff,
        "month_for_tariff": month_for_tariff,
        "day_for_tariff": day_for_tariff,
        "specific_van_for_coal_id": specific_van_for_coal_id,
        "mainland_payment_by_loaded_carriage": mainland_payment_by_loaded_carriage,
        "sakhalin_payment_by_loaded_carriage": sakhalin_payment_by_loaded_carriage,
        "crimea_payment_by_loaded_carriage": crimea_payment_by_loaded_carriage,
        "kazakhstan_payment_by_loaded_carriage": kazakhstan_payment_by_loaded_carriage,
        "litva_payment_by_loaded_carriage": litva_payment_by_loaded_carriage,
        "belarus_payment_by_loaded_carriage": belarus_payment_by_loaded_carriage,
        "zhdn_payment_by_loaded_carriage": zhdn_payment_by_loaded_carriage,
        "mainland_payment_by_empty_carriage": mainland_payment_by_empty_carriage,
        "sakhalin_payment_by_empty_carriage": sakhalin_payment_by_empty_carriage,
        "crimea_payment_by_empty_carriage": crimea_payment_by_empty_carriage,
        "kazakhstan_payment_by_empty_carriage": kazakhstan_payment_by_empty_carriage,
        "litva_payment_by_empty_carriage": litva_payment_by_empty_carriage,
        "belarus_payment_by_empty_carriage": belarus_payment_by_empty_carriage,
        "zhdn_payment_by_empty_carriage": zhdn_payment_by_empty_carriage,
        "mainland_payment_distance": mainland_payment_distance,
        "sakhalin_payment_distance": sakhalin_payment_distance,
        "crimea_payment_distance": crimea_payment_distance,
        "kazakhstan_payment_distance": kazakhstan_payment_distance,
        "litva_payment_distance": litva_payment_distance,
        "belarus_payment_distance": belarus_payment_distance,
        "zhdn_payment_distance": zhdn_payment_distance,
        "mainland_currency_of_result": mainland_currency_of_result,
        "sakhalin_currency_of_result": sakhalin_currency_of_result,
        "crimea_currency_of_result": crimea_currency_of_result,
        "kazakhstan_currency_of_result": kazakhstan_currency_of_result,
        "litva_currency_of_result": litva_currency_of_result,
        "belarus_currency_of_result": belarus_currency_of_result,
        "zhdn_currency_of_result": zhdn_currency_of_result,
        "date_calculation": date_calculation,
        "ETSNG_to_avoid": ETSNG_to_avoid,
        "station_otpr_name_in_system": station_otpr_name_in_system,
        "station_nazn_name_in_system": station_nazn_name_in_system,
        "station_otpr_subject_RF": station_otpr_subject_RF,
        "station_otpr_region": station_otpr_region,
        "station_otpr_polygon": station_otpr_polygon,
        "station_nazn_subject_RF": station_nazn_subject_RF,
        "station_nazn_region": station_nazn_region,
        "station_nazn_polygon": station_nazn_polygon,
    }

    # Проверяем, существует ли поле
    if not hasattr(Corr, field):
        available_fields = ", ".join([col.key for col in Corr.__table__.columns])
        raise HTTPException(
            status_code=400,
            detail=f"Поле '{field}' не существует. Доступные поля: {available_fields}"
        )

    result = connect_to_db.query(Corr)

    for attr, value in filters.items():
        if value is not None:
            result = result.filter(getattr(Corr, attr) == value)

    # Получаем уникальные значения для указанного поля
    unique_values = (
        result
        .with_entities(getattr(Corr, field))  # Выбираем ТОЛЬКО нужное поле
        .filter(getattr(Corr, field) != None)  # Исключаем NULL
        .filter(getattr(Corr, field) != "")    # Исключаем пустые строки
        .distinct()
        .order_by(getattr(Corr, field))        # Сортируем по алфавиту
        .all()
    )

    # Например
    # http://localhost:8889/unique_values/esr_otpr - вернет уникальные ЕСР отправления
    # http://localhost:8889/unique_values/esr_otpr?station_otpr_region=Уральский&year_for_tariff=2022
    # вернёт уникальные ЕСР отправления где регион станции отправления был Уральский, а год для расчёта тарифа - 2022

    # Преобразуем результат в простой список
    return [value[0] for value in unique_values]