import requests

from related_funcs_and_variables.confidentials import url_to_etran_backend
from related_funcs_and_variables.confidentials import (
    login_to_etran_backend,
    password_to_etran_backend,
)
from related_funcs_and_variables.sensitive_data import (
    type_of_car_map,
    esr_and_country_map,
)


def send_xml_post_request(mobj, timeout=10):
    """Отправляет POST-запрос с XML, сформированным через f-строку"""

    # Приведение формата даты к ДДММГГГГ
    date_calculation = (
        mobj.day_for_tariff + "." + mobj.month_for_tariff + "." + mobj.year_for_tariff
    )

    # Это костыль пока что, так как конечные данные будут идти из сервера и неясен формат и наполнение
    # 1 - повагонная, 2 - контейнерная, 4 - групповая, 5 - маршрутная
    query_type_dispatch = "1"
    if mobj.type_dispatch.lower() == "г":
        query_type_dispatch = "4"
    elif mobj.type_dispatch.lower() == "м":
        query_type_dispatch = "5"
    elif mobj.type_dispatch.lower() == "к":
        query_type_dispatch = "2"

    # Если type_dispatch = 1, 2 или 4, то, если нужно отправить одиночный контейнер, в поле pINV_RouteType_ID нужно
    # ничего не писать, передать пустой аргумент.
    # Если type_dispatch = 5, то в поле pINV_RouteType_ID нужно поставить 1.
    route_type = ""
    # Проверка на is_container_train потому что в исходных данных может быть контейнер, но не контейнерный поезд
    if query_type_dispatch == "5" or mobj.is_container_train == "1":
        route_type = "1"

    type_of_car = str(type_of_car_map[mobj.type_of_car.lower()])

    country_from = "178"
    country_to = "178"

    if mobj.esr_otpr in esr_and_country_map:
        country_from = esr_and_country_map[mobj.esr_otpr]
    if mobj.esr_nazn in esr_and_country_map:
        country_to = str(esr_and_country_map[mobj.esr_nazn])

    # Временная заглушка
    type_of_cont = "G0"
    length_of_cont = "20"

    not_container_xml_data_query = f"""<?xml version="1.0" encoding="utf-8"?>
                <soapenv:Envelope 
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:sys="SysEtranInt"><soapenv:Header/><soapenv:Body>
                <sys:GetBlock>
                <Login>{login_to_etran_backend}</Login>
                <Password>{password_to_etran_backend}</Password>
                <Text><EtranTranspPayment>
                <pINV_SendKind_ID>{query_type_dispatch}</pINV_SendKind_ID>
                <pINV_Speed_ID>2</pINV_Speed_ID>
                <pINV_RouteType_ID>{route_type}</pINV_RouteType_ID> 
                <pINV_AnnounceValue>0</pINV_AnnounceValue>
                <pINV_Date_Load>{date_calculation}</pINV_Date_Load>
                <pINV_PlanOwnerTypeCar_ID>1</pINV_PlanOwnerTypeCar_ID>
                <pINV_Plan_Cont_OwnerType_ID>1</pINV_Plan_Cont_OwnerType_ID>
                <pINV_Loadassets_ID>1</pINV_Loadassets_ID>
                <pINV_Unloadassets_ID>1</pINV_Unloadassets_ID>
                <Goods>
                <pGDS_FREIGHTCODE>{mobj.etsng_cargo}</pGDS_FREIGHTCODE>
                <pGDS_WeightReal></pGDS_WeightReal>
                <pGDS_DangerSign_ID>1</pGDS_DangerSign_ID>
                </Goods>
                <Wag>
                <pWAG_Count>{mobj.cars_amount_in_train}</pWAG_Count>
                <pWAG_OWNERTYPE_ID>1</pWAG_OWNERTYPE_ID>
                <pWAG_Axles>4</pWAG_Axles>
                <pWAG_Tonnage>{mobj.car_dead_weight}</pWAG_Tonnage>
                <pWAG_WEIGHTDEP>245</pWAG_WEIGHTDEP>
                <pWAG_WEIGHTNET>{str(int(mobj.mass_in_car)*1000)}</pWAG_WEIGHTNET>
                <pWAG_WagType_Id>{type_of_car}</pWAG_WagType_Id>
                <pWag_OwnerCountry_Id>178</pWag_OwnerCountry_Id>
                <pWAG_LENGTH>13.92</pWAG_LENGTH>
                </Wag>
                <Distances>
                <pDST_COUNTRY_ID>{country_from}</pDST_COUNTRY_ID>
                <pDST_ORDERNUMBER>1</pDST_ORDERNUMBER>
                <pDST_stationCode>{mobj.esr_otpr}</pDST_stationCode>
                </Distances>
                <Distances>
                <pDST_COUNTRY_ID>{country_to}</pDST_COUNTRY_ID>
                <pDST_ORDERNUMBER>2</pDST_ORDERNUMBER>
                <pDST_stationCode>{mobj.esr_nazn}</pDST_stationCode>
                </Distances>
                <CndBlock>
                <pCND_TRANSPCLAUSE_ID>398</pCND_TRANSPCLAUSE_ID>
                <pCND_CustomText>2</pCND_CustomText>
                </CndBlock>
                </EtranTranspPayment>
                </Text></sys:GetBlock></soapenv:Body></soapenv:Envelope>"""

    container_xml_data_query = f"""<?xml version="1.0" encoding="utf-8"?>
                <soapenv:Envelope 
                xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" 
                xmlns:sys="SysEtranInt"><soapenv:Header/><soapenv:Body>
                <sys:GetBlock>
                <Login>{login_to_etran_backend}</Login>
                <Password>{password_to_etran_backend}</Password>
                <Text><EtranTranspPayment>
                <pINV_SendKind_ID>{query_type_dispatch}</pINV_SendKind_ID>
                <pINV_Speed_ID>2</pINV_Speed_ID>
                <pINV_RouteType_ID>{route_type}</pINV_RouteType_ID>
                <pINV_AnnounceValue>0</pINV_AnnounceValue>
                <pINV_Date_Load>{date_calculation}</pINV_Date_Load>
                <pINV_PlanOwnerTypeCar_ID>1</pINV_PlanOwnerTypeCar_ID>
                <pINV_Plan_Cont_OwnerType_ID>1</pINV_Plan_Cont_OwnerType_ID>
                <pINV_Loadassets_ID>1</pINV_Loadassets_ID>
                <pINV_Unloadassets_ID>1</pINV_Unloadassets_ID>
                <Goods>
                <pGDS_FREIGHTCODE>{mobj.etsng_cargo}</pGDS_FREIGHTCODE>
                <pGDS_WeightReal></pGDS_WeightReal>
                <pGDS_DangerSign_ID>1</pGDS_DangerSign_ID>
                </Goods>
                <Wag>
                <pWAG_Count>{mobj.cars_amount_in_train}</pWAG_Count>
                <pWAG_OWNERTYPE_ID>1</pWAG_OWNERTYPE_ID>
                <pWAG_Axles>4</pWAG_Axles>
                <pWAG_Tonnage>{mobj.car_dead_weight}</pWAG_Tonnage>
                <pWAG_WEIGHTDEP>245</pWAG_WEIGHTDEP>
                <pWAG_WEIGHTNET>{str(int(mobj.mass_in_car)*1000)}</pWAG_WEIGHTNET>
                <pWAG_WagType_Id>{type_of_car}</pWAG_WagType_Id>
                <pWag_OwnerCountry_Id>178</pWag_OwnerCountry_Id>
                <pWAG_LENGTH>13.92</pWAG_LENGTH>
                </Wag>
                <Container>
                <pCNT_OWNERTYPE_ID>1</pCNT_OWNERTYPE_ID>
                <pCNT_WEIGHTDEP>3000</pCNT_WEIGHTDEP>
                <pCNT_WEIGHTNET>{str(int(mobj.mass_in_car)*1000)}</pCNT_WEIGHTNET>
                <pCNT_TONNAGEVALUE>{mobj.car_dead_weight}</pCNT_TONNAGEVALUE>
                <pCNT_TypeCode>{type_of_cont}</pCNT_TypeCode>
                <pCNT_WIDTH_F>{length_of_cont}</pCNT_WIDTH_F>
                <pCNT_OwnerCountry_Id>178</pCNT_OwnerCountry_Id>
                </Container>
                <Distances>
                <pDST_COUNTRY_ID>178</pDST_COUNTRY_ID>
                <pDST_ORDERNUMBER>1</pDST_ORDERNUMBER>
                <pDST_stationCode>{mobj.esr_otpr}</pDST_stationCode>
                </Distances>
                <Distances>
                <pDST_COUNTRY_ID>178</pDST_COUNTRY_ID>
                <pDST_ORDERNUMBER>2</pDST_ORDERNUMBER>
                <pDST_stationCode>{mobj.esr_nazn}</pDST_stationCode>
                </Distances>
                <CndBlock>
                <pCND_TRANSPCLAUSE_ID>398</pCND_TRANSPCLAUSE_ID>
                <pCND_CustomText>2</pCND_CustomText>
                </CndBlock>
                </EtranTranspPayment>
                </Text></sys:GetBlock></soapenv:Body></soapenv:Envelope>"""

    headers = {
        "Content-Type": "application/xml; charset=utf-8",
        "Accept": "application/xml",
    }

    if mobj.is_container_train == "0":
        query_params = not_container_xml_data_query
    else:
        query_params = container_xml_data_query

    try:
        response = requests.post(
            url=url_to_etran_backend,
            data=query_params.encode("utf-8"),  # Преобразуем в байты
            headers=headers,
            timeout=timeout,
        )

        response.raise_for_status()

        # 20 символов - это отступ от начала среза строки, включающий в себя текст MainPayLoadedWag&gt
        # 4 символа - это отступ от конца строки, включающий в себя текст, например, 35240&lt;
        # 19 символов это отступ от конца строки, включающий в себя текст MainPayEmptyWag&gt;
        # 4 символа - это отступ от конца строки, включающий в себя текст, например, 24914&lt;
        loaded_pay = response.text[
            response.text.find("MainPayLoadedWag")
            + 20 : response.text.find("/MainPayLoadedWag")
            - 4
        ]
        empty_pay = response.text[
            response.text.find("MainPayEmptyWag")
            + 19 : response.text.find("/MainPayEmptyWag")
            - 4
        ]
        add_pay_loaded = response.text[
            response.text.find("AddPayLoadedWag")
            + 19 : response.text.find("/AddPayLoadedWag")
            - 4
        ]
        add_pay_empty = response.text[
            response.text.find("AddPayEmptyWag")
            + 18 : response.text.find("/AddPayEmptyWag")
            - 4
        ]
        min_way = response.text[
            response.text.find("MinWay") + 10 : response.text.find("/MinWay") - 4
        ]

        print(
            "Плата за груженый вагон:",
            loaded_pay,
            "Плата за порожний вагон:",
            empty_pay,
            "Дополнительный платеж за груженый вагон:",
            add_pay_loaded,
            "Дополнительный платеж за порожний вагон:",
            add_pay_empty,
            "Тарифное расстояние:",
            min_way,
            sep="\n",
        )

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при отправке запроса: {str(e)}")
        raise
