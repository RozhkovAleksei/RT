from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from RelatedFunctionsAndVariables.externals import db_filename, table_name

sql_alchemy_db_url = "sqlite:///"+db_filename

engine = create_engine(sql_alchemy_db_url)
my_session_fabric = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

class Corr(Base):
    __tablename__ = table_name
    id = Column(Integer, primary_key=True, autoincrement=True)
    esr_otpr = Column(String)
    station_otpr_name = Column(String)
    esr_nazn = Column(String)
    station_nazn_name = Column(String)
    type_dispatch = Column(String)
    is_container_train = Column(String)
    etsng_cargo = Column(String)
    mass_in_car = Column(String)
    type_of_container = Column(String)
    type_of_car = Column(String)
    car_dead_weight = Column(String)
    cars_amount_in_train = Column(String)
    year_for_tariff = Column(String)
    month_for_tariff = Column(String)
    day_for_tariff = Column(String)
    specific_van_for_coal_id = Column(String)
    mainland_payment_by_loaded_carriage = Column(String)
    mainland_payment_by_empty_carriage = Column(String)
    mainland_payment_distance = Column(String)
    sakhalin_payment_by_loaded_carriage = Column(String)
    sakhalin_payment_by_empty_carriage = Column(String)
    sakhalin_payment_distance = Column(String)
    crimea_payment_by_loaded_carriage = Column(String)
    crimea_payment_by_empty_carriage = Column(String)
    crimea_payment_distance = Column(String)
    kazakhstan_payment_by_loaded_carriage = Column(String)
    kazakhstan_payment_by_empty_carriage = Column(String)
    kazakhstan_payment_distance = Column(String)
    litva_payment_by_loaded_carriage = Column(String)
    litva_payment_by_empty_carriage = Column(String)
    litva_payment_distance = Column(String)
    belarus_payment_by_loaded_carriage = Column(String)
    belarus_payment_by_empty_carriage = Column(String)
    belarus_payment_distance = Column(String)
    zhdn_payment_by_loaded_carriage = Column(String)
    zhdn_payment_by_empty_carriage = Column(String)
    zhdn_payment_distance = Column(String)
    mainland_currency_of_result = Column(String)
    sakhalin_currency_of_result = Column(String)
    crimea_currency_of_result = Column(String)
    kazakhstan_currency_of_result = Column(String)
    litva_currency_of_result = Column(String)
    belarus_currency_of_result = Column(String)
    zhdn_currency_of_result = Column(String)
    date_calculation = Column(String)
    ETSNG_to_avoid = Column(String)
    station_otpr_name_in_system = Column(String)
    station_nazn_name_in_system = Column(String)
    station_otpr_subject_RF = Column(String)
    station_otpr_region = Column(String)
    station_otpr_polygon = Column(String)
    station_nazn_subject_RF = Column(String)
    station_nazn_region = Column(String)
    station_nazn_polygon = Column(String)

    def to_dict(self):
        return{col.name: getattr(self, col.name) for col in self.__table__.columns}

    def __repr__(self):
        return (f"id={self.id!r}, "
                f"esr_otpr={self.esr_otpr!r}, "
                f"station_otpr_name={self.station_otpr_name!r}, "
                f"esr_nazn={self.esr_nazn!r}, "
                f"station_nazn_name={self.station_nazn_name!r}, "
                f"type_dispatch={self.type_dispatch!r}, "
                f"is_container_train={self.is_container_train!r}, "
                f"etsng_cargo={self.etsng_cargo!r}, "
                f"mass_in_car={self.mass_in_car!r}, "
                f"type_of_container={self.type_of_container!r}, "
                f"type_of_car={self.type_of_car!r}, "
                f"car_dead_weight={self.car_dead_weight!r}, "
                f"cars_amount_in_train={self.cars_amount_in_train!r}, "
                f"year_for_tariff={self.year_for_tariff!r}, "
                f"month_for_tariff={self.month_for_tariff!r}, "
                f"day_for_tariff={self.day_for_tariff!r}, "
                f"specific_van_for_coal_id={self.specific_van_for_coal_id!r}, "
                f"mainland_payment_by_loaded_carriage={self.mainland_payment_by_loaded_carriage!r}, "
                f"mainland_payment_by_empty_carriage={self.mainland_payment_by_empty_carriage!r}, "
                f"mainland_payment_distance={self.mainland_payment_distance!r}, "
                f"sakhalin_payment_by_loaded_carriage={self.sakhalin_payment_by_loaded_carriage!r}, "
                f"sakhalin_payment_by_empty_carriage={self.sakhalin_payment_by_empty_carriage!r}, "
                f"sakhalin_payment_distance={self.sakhalin_payment_distance!r}, "
                f"crimea_payment_by_loaded_carriage={self.crimea_payment_by_loaded_carriage!r}, "
                f"crimea_payment_by_empty_carriage={self.crimea_payment_by_empty_carriage!r}, "
                f"crimea_payment_distance={self.crimea_payment_distance!r}, "
                f"kazakhstan_payment_by_loaded_carriage={self.kazakhstan_payment_by_loaded_carriage!r}, "
                f"kazakhstan_payment_by_empty_carriage={self.kazakhstan_payment_by_empty_carriage!r}, "
                f"kazakhstan_payment_distance={self.kazakhstan_payment_distance!r}, "
                f"litva_payment_by_loaded_carriage={self.litva_payment_by_loaded_carriage!r}, "
                f"litva_payment_by_empty_carriage={self.litva_payment_by_empty_carriage!r}, "
                f"litva_payment_distance={self.litva_payment_distance!r}, "
                f"belarus_payment_by_loaded_carriage={self.belarus_payment_by_loaded_carriage!r}, "
                f"belarus_payment_by_empty_carriage={self.belarus_payment_by_empty_carriage!r}, "
                f"belarus_payment_distance={self.belarus_payment_distance!r}, "
                f"zhdn_payment_by_loaded_carriage={self.zhdn_payment_by_loaded_carriage!r}, "
                f"zhdn_payment_by_empty_carriage={self.zhdn_payment_by_empty_carriage!r}, "
                f"zhdn_payment_distance={self.zhdn_payment_distance!r}, "
                f"mainland_currency_of_result={self.mainland_currency_of_result!r}, "
                f"sakhalin_currency_of_result={self.sakhalin_currency_of_result!r}, "
                f"crimea_currency_of_result={self.crimea_currency_of_result!r}, "
                f"kazakhstan_currency_of_result={self.kazakhstan_currency_of_result!r}, "
                f"litva_currency_of_result={self.litva_currency_of_result!r}, "
                f"belarus_currency_of_result={self.belarus_currency_of_result!r}, "
                f"zhdn_currency_of_result={self.zhdn_currency_of_result!r}, "
                f"date_calculation={self.date_calculation!r}, "
                f"ETSNG_to_avoid={self.ETSNG_to_avoid!r}, "
                f"station_otpr_name_in_system={self.station_otpr_name_in_system!r}, "
                f"station_nazn_name_in_system={self.station_nazn_name_in_system!r}, "
                f"station_otpr_subject_RF={self.station_otpr_subject_RF!r}, "
                f"station_otpr_region={self.station_otpr_region!r}, "
                f"station_otpr_polygon={self.station_otpr_polygon!r}, "
                f"station_nazn_subject_RF={self.station_nazn_subject_RF!r}, "
                f"station_nazn_region={self.station_nazn_region!r}, "
                f"station_nazn_polygon={self.station_nazn_polygon!r}")

    # Когда понадобится создать таблицу при первом запуске
    # Base.metadata.create_all(engine)
