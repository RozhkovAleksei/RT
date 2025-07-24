from pandas import to_numeric
import pyautogui as pag
import keyboard
from time import sleep
import globals as gl
from externals import sleep_short, sleep_long
from loguru import logger

@logger.catch(reraise=True)
def set_car_type_capacity_amount_in_group(mobj):

    # Блок вызова окна с вводом типа подвижного состава
    gl.SetRailTariffWindowActiveForInput(6)
    sleep(sleep_long)

    # Предположительно - курсор уже будет стоять в поле, где надо ввести тип контейнера.
    if mobj.type_dispatch.lower() == 'к':
        keyboard.write(mobj.type_of_container)
        sleep(sleep_long)
        pag.press('tab')
        sleep(sleep_short)
        pag.press('tab')
        sleep(sleep_long)
        pag.press('space')
        sleep(sleep_long)
        pag.press('enter')
        sleep(sleep_long)

        # При перевозке в контейнерах, помимо самого контейнера ещё нужно выбрать платформу.
        gl.SetRailTariffWindowActiveForInput(9)

        sleep(sleep_long)
        keyboard.write(mobj.type_of_car)
        sleep(sleep_long)
        pag.press('tab')
        sleep(sleep_short)
        pag.press('tab')
        sleep(sleep_long)
        pag.press('space')
        sleep(sleep_long)

    # Обособленная проверка на тип вагона "крытый" стоит потому, что по умолчанию RT ставит вагон крытым и клик на метке вагона
    # закроет поле для ввода данных о грузоподъемности вагона и программа остановится и порушит дальнейшее выполнение расчетов
    # вместе с тем, если ранее не сработает блок кода, который начинает каждый раз новый расчет - то если надо будет считать
    # корреспонденцию с крытым вагоном, а перед этим расчетом будет другой вагон (не крытый) - расчет сломается.
    if mobj.type_dispatch.lower() != 'к' and mobj.type_of_car.lower() != 'крытый':
        # блок ввода типа подвижного состава
        keyboard.write(mobj.type_of_car)
        sleep(sleep_short)
        pag.press('tab')
        pag.press('tab')
        sleep(sleep_short)
        pag.press('space')
        sleep(sleep_short)
        # Блок ввода грузоподъемности вагона
        pag.press('tab')
        pag.press('tab')
        sleep(sleep_short)
        pag.press('del')
        # for i in range(0, 5):
        #     sleep(sleep_moment)
        #     pag.press('del')
        keyboard.write(mobj.car_dead_weight, delay=0.01)
        sleep(sleep_short)

        # Для расчета в условиях 2021 года нужно посчитать по специфическим полувагонам
        if to_numeric(mobj.car_dead_weight) >= int('75') and mobj.type_of_car.lower() == "полувагон":
            if mobj.year_for_tariff == "2021":
                for i in range(0, 2):
                    sleep(sleep_short)
                    pag.press('tab')  # курсор переводится к окну с выбором серии полувагона

                if mobj.specific_van_for_coal_id == "12 196-01" or mobj.specific_van_for_coal_id == "12 196-02":
                    for i in range(0, 2):  # данный вагон 1 в списке, но 2 раза стрелку вниз
                        sleep(sleep_short)
                        pag.press('down')
                    sleep(sleep_short)
                    pag.press('enter')
                if mobj.specific_van_for_coal_id == "12 9761-02":
                    for i in range(0, 6):  # данный вагон 5 в списке, но 6 раз стрелку вниз
                        sleep(sleep_short)
                        pag.press('down')
                    sleep(sleep_short)
                    pag.press('enter')

                # В данном месте вагон выбран, курсор на поле с выбором вагона

                for i in range(0, 2):
                    sleep(sleep_short)
                    pag.hotkey('shiftleft', 'tab')  # Курсор возвращается к окну с грузоподъемностью
            else:
                # Почему здесь было присвоение типа вагона именно 12 196-01?
                mobj.specific_van_for_coal_id = "12 196-01"
                for i in range(0, 2):
                    sleep(sleep_short)
                    pag.press('tab')
                for i in range(0, 2):
                    sleep(sleep_short)
                    pag.press('down')
                sleep(sleep_short)
                pag.press('enter')

                for i in range(0, 6):
                    sleep(sleep_short)
                    pag.press('tab')

    elif mobj.type_of_car.lower() == 'крытый':
        # Здесь если тип вагона - крытый
        for i in range(0, 4):
            sleep(sleep_short)
            pag.press('tab')
        pag.press('del')
        sleep(sleep_short)
        pag.typewrite(mobj.car_dead_weight)
    else:
        print("Вагон не крытый и не полувагон")

    if mobj.type_dispatch.lower() == 'г':
        for i in range(0, 7):
            sleep(sleep_short)
            pag.hotkey('shiftleft', 'tab')
        sleep(sleep_short)
        pag.typewrite(mobj.cars_amount_in_train)
        sleep(sleep_short)

    pag.press('enter')

    sleep(sleep_short)

