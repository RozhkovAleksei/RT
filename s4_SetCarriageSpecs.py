from pandas import to_numeric
import pyautogui as pag
import keyboard
from time import sleep
import globals


def SetCarriageTypeCapacityAmountInGroup(carriage_type, container_type, capacity, amount_in_group, type_of_dispatch, mobj):

    # Блок вызова окна с вводом типа подвижного состава
    globals.SetRailTariffWindowActiveForInput(6)
    sleep(mobj.global_sleep_long)

    # Предположительно - курсор уже будет стоять в поле, где надо ввести тип контейнера.
    if type_of_dispatch.lower() == 'к':
        keyboard.write(str(container_type))
        sleep(mobj.global_sleep_long)
        pag.press('tab')
        sleep(mobj.global_sleep_short)
        pag.press('tab')
        sleep(mobj.global_sleep_long)
        pag.press('space')
        sleep(mobj.global_sleep_long)
        pag.press('enter')
        sleep(mobj.global_sleep_long)

        # При перевозке в контейнерах, помимо самого контейнера ещё нужно выбрать платформу.
        globals.SetRailTariffWindowActiveForInput(9)

        sleep(mobj.global_sleep_long)
        keyboard.write(str(carriage_type))
        sleep(mobj.global_sleep_long)
        pag.press('tab')
        sleep(mobj.global_sleep_short)
        pag.press('tab')
        sleep(mobj.global_sleep_long)
        pag.press('space')
        sleep(mobj.global_sleep_long)

    # Обособленная проверка на тип вагона "крытый" стоит потому, что по умолчанию RT ставит вагон крытым и клик на метке вагона
    # закроет поле для ввода данных о грузоподъемности вагона и программа остановится и порушит дальнейшее выполнение расчетов
    # вместе с тем, если ранее не сработает блок кода, который начинает каждый раз новый расчет - то если надо будет считать
    # корреспонденцию с крытым вагоном, а перед этим расчетом будет другой вагон (не крытый) - расчет сломается.
    if type_of_dispatch.lower() != 'к' and carriage_type.lower() != 'крытый':
        # блок ввода типа подвижного состава
        keyboard.write(str(carriage_type))
        sleep(mobj.global_sleep_short)
        pag.press('tab')
        pag.press('tab')
        sleep(mobj.global_sleep_short)
        pag.press('space')
        sleep(mobj.global_sleep_short)
        # Блок ввода грузоподъемности вагона
        pag.press('tab')
        pag.press('tab')
        sleep(mobj.global_sleep_short)
        pag.press('del')
        # for i in range(0, 5):
        #     sleep(mobj.global_sleep_moment)
        #     pag.press('del')
        keyboard.write(capacity, delay=0.01)
        sleep(mobj.global_sleep_short)

        # Для расчета в условиях 2021 года нужно посчитать по специфическим полувагонам
        if to_numeric(capacity) >= int('75') and carriage_type.lower() == "полувагон":
            if mobj.calc_year == "2021":
                for i in range(0, 2):
                    sleep(mobj.global_sleep_short)
                    pag.press('tab')  # курсор переводится к окну с выбором серии полувагона

                if mobj.specific_van_for_coal_id == "12 196-01" or mobj.specific_van_for_coal_id == "12 196-02":
                    for i in range(0, 2):  # данный вагон 1 в списке, но 2 раза стрелку вниз
                        sleep(mobj.global_sleep_short)
                        pag.press('down')
                    sleep(mobj.global_sleep_short)
                    pag.press('enter')
                if mobj.specific_van_for_coal_id == "12 9761-02":
                    for i in range(0, 6):  # данный вагон 5 в списке, но 6 раз стрелку вниз
                        sleep(mobj.global_sleep_short)
                        pag.press('down')
                    sleep(mobj.global_sleep_short)
                    pag.press('enter')

                # В данном месте вагон выбран, курсор на поле с выбором вагона

                for i in range(0, 2):
                    sleep(mobj.global_sleep_short)
                    pag.hotkey('shiftleft', 'tab')  # Курсор возвращается к окну с грузоподъемностью
            else:
                # Почему здесь было присвоение типа вагона именно 12 196-01?
                mobj.specific_van_for_coal_id = "12 196-01"
                for i in range(0, 2):
                    sleep(mobj.global_sleep_short)
                    pag.press('tab')
                for i in range(0, 2):
                    sleep(mobj.global_sleep_short)
                    pag.press('down')
                sleep(mobj.global_sleep_short)
                pag.press('enter')

                for i in range(0, 6):
                    sleep(mobj.global_sleep_short)
                    pag.press('tab')

    elif carriage_type.lower() == 'крытый':
        # Здесь если тип вагона - крытый
        for i in range(0, 4):
            sleep(mobj.global_sleep_short)
            pag.press('tab')
        pag.press('del')
        sleep(mobj.global_sleep_short)
        pag.typewrite(str(capacity))
    else:
        print("Вагон не крытый и не полувагон")

    if type_of_dispatch.lower() == 'г':
        for i in range(0, 7):
            sleep(mobj.global_sleep_short)
            pag.hotkey('shiftleft', 'tab')
        sleep(mobj.global_sleep_short)
        pag.typewrite(amount_in_group)
        sleep(mobj.global_sleep_short)

    pag.press('enter')

    sleep(mobj.global_sleep_short)

