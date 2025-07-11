import pyautogui as pag
import keyboard
from time import sleep
import globals
import win32gui


def SetETSNGCodeAndMassInCarriage(ETSNG_code, mass_in_carriage, mobj):

    globals.SetRailTariffWindowActiveForInput(5)

    sleep(mobj.global_sleep_short)

    # Ищется вкладка с полем для ввода кода ГНГ. Если найдено, то переключается на ЕТСНГ
    try:
        wnd = win32gui.FindWindow(None, "Груз")

        wnd_coord = win32gui.GetWindowRect(wnd)

        if wnd != 0:
            globals.SetRailTariffWindowActive()
            for i in range(999, 0, -1):
                tmp_conf = float(i/1000)
                gng_code_set = pag.locateOnScreen(mobj.path_to_img_data + "Gng_short.png",
                                                    confidence=tmp_conf, region=(wnd_coord[0],wnd_coord[1],
                                                                                    wnd_coord[2]-wnd_coord[0],
                                                                                    wnd_coord[3]-wnd_coord[1]),
                                                    limit=1, grayscale=True,
                                                    minSearchTime=mobj.min_search_time)
                # print(gng_code_set)

                if gng_code_set is not None:
                    # Если местоположение изображения нашлось - выходим из цикла
                    # print("Местоположение gng_code_set найдено по координатам:", gng_code_set)
                    globals.SetRailTariffWindowActive()
                    pag.hotkey('shift', 'tab')
                    sleep(mobj.global_sleep_short)
                    pag.hotkey('shift', 'tab')
                    sleep(mobj.global_sleep_short)
                    pag.press('left')
                    sleep(mobj.global_sleep_short)
                    pag.press('space')
                    # break
                # else:
                #     print("gng_code_set is None")
                #     globals.ExitByError()

            sleep(mobj.global_sleep_short)

            # Проверка, что переключение на ЕТСНГ прошло корректно
            try:
                for j in range(999, 0, -1):
                    tmp_conf = float(j/1000)
                    etsng_code_set = pag.locateOnScreen(mobj.path_to_img_data + "ETSNG_short.png",
                                                        confidence=tmp_conf, region=(wnd_coord[0],wnd_coord[1],
                                                                                        wnd_coord[2]-wnd_coord[0],
                                                                                        wnd_coord[3]-wnd_coord[1]),
                                                        limit=1, grayscale=True,
                                                        minSearchTime=mobj.min_search_time)

                    # print(etsng_code_set)

                    # Если не найдено, то предположение, что переключение по каким-то причинам не прошло
                    if etsng_code_set is None:
                        pag.hotkey('shiftleft', 'tab')
                        sleep(mobj.global_sleep_short)
                        pag.hotkey('shiftleft', 'tab')
                        sleep(mobj.global_sleep_short)
                        pag.press('left')
                        sleep(mobj.global_sleep_short)
                        pag.press('space')
                    else:
                        # print("ЕТСНГ найдено")
                        continue
            except Exception as ESTNG_code_set_excp:
                print("ESTNG_code_set_excp", ESTNG_code_set_excp)
                # print("Переключение на ЕТСНГ не прошло либо не нашлось на экране")

            sleep(mobj.global_sleep_short)

    except Exception as GNG_code_extended_excp:
        print("GNG_code_extended_excp", GNG_code_extended_excp)
        # print("Курсор не на ГНГ либо не нашлось на экране")
        # Здесь указан pass, потому что ненахождение окна не всегда является проблемой.
        # Иногда блок ввода кода уже стоит на ЕТСНГ,16 поэтому ГНГ не будет найден и не нужно его искать.
        pass

    sleep(mobj.global_sleep_long)

    # Вставляется код ЕТСНГ груза, чтобы по фильтру ниже в окне появилось её название
    # На всякий случай активируется окно
    globals.SetRailTariffWindowActive()
    keyboard.write(str(ETSNG_code), delay=mobj.duration_for_test_purposes)
    sleep(mobj.global_sleep_long)

    # Проходим по окну до поля ввода массы груза в вагоне
    for i in range(0, 4):
        sleep(mobj.global_sleep_long)
        pag.press('tab')
    sleep(mobj.global_sleep_short)
    keyboard.write(mass_in_carriage, delay=mobj.duration_for_test_purposes)
    sleep(mobj.global_sleep_short)

    # Нажимаем Enter для ввода параметров. Если что-то не так - всплывёт окно
    pag.press('enter')
    sleep(mobj.global_sleep_long)

    #Если всё прошло нормально - окно с вводом кода груза закрылось и данные приняты для расчёта.

    # Проверяем, что всплывает неименованное окно с предупреждением о необходимости выбора кода ГНГ
    if win32gui.GetForegroundWindow() != 0 and win32gui.GetWindowText(win32gui.GetForegroundWindow()) == ' ':
        # print("Появилось неименованное окно о выборе кода ГНГ")
        # Собираем нежелательный код ЕТСНГ в атрибут объекта класса для дальнейшего вывода на печать
        mobj.ETSNG_to_avoid = ETSNG_code
        pag.press('esc')
        sleep(mobj.global_sleep_short)

        is_gng_code_defined = globals.gng_extra_option_finder(mobj)

        if is_gng_code_defined == 'gng_not_defined':
            pag.press('esc')
            sleep(mobj.global_sleep_long)
            pag.press('down')
            sleep(mobj.global_sleep_long)
            pag.press('enter')

            # print("Повторно появилось неименованное окно о выборе кода ГНГ")
            if win32gui.GetForegroundWindow() != 0 and win32gui.GetWindowText(win32gui.GetForegroundWindow()) == ' ':
                # Собираем нежелательный код ЕТСНГ в атрибут объекта класса для дальнейшего вывода на печать
                mobj.ETSNG_to_avoid = ETSNG_code
                pag.press('esc')
                sleep(mobj.global_sleep_long)

                # При повторном появлении неименованного окна о выборе кода ГНГ после того, как выполнен шаг вниз
                # по списку после предыдущего невалидного кода - (!)ПРЕДПОЛОЖИТЕЛЬНО(!) выбран валидный код ГНГ
                # Соответственно, если код валидный, просто выбираем его из списка и заканчиваем ввод в этом окне
                # Если повторно попали на невалидный код ГНГ - снова выходим и шагаем вниз.
                # Иначе - если дважды не можем найти валидный код - выходим из текущей итерации расчёта и переходим
                # к следующей. Кейс с двойным невалидным кодом ГНГ - это какой-то форс-мажор и надо разбираться!
                if globals.gng_extra_option_finder(mobj) == 'gng_defined':
                    pag.press('enter')
                    sleep(mobj.global_sleep_short)
                    pag.press('enter')
                    sleep(mobj.global_sleep_short)

                elif globals.gng_extra_option_finder(mobj) == 'gng_not_defined':
                    pag.press('esc')
                    sleep(mobj.global_sleep_short)
                    pag.press('down')
                    sleep(mobj.global_sleep_short)
                    pag.press('enter')

                    if win32gui.GetForegroundWindow() != 0 and win32gui.GetWindowText(
                            win32gui.GetForegroundWindow()) == ' ':
                        globals.SetRailTariffWindowActive()
                        print("Дважды невалидный код ГНГ - нужно детально разбираться с корреспонденцией!!")
                        globals.ExitByError()
                    else:
                        sleep(mobj.global_sleep_short)
                        pag.press('enter')

            else:
                sleep(mobj.global_sleep_short)
                pag.press('enter')

        elif is_gng_code_defined == 'gng_defined':
            pag.press('enter')
            sleep(mobj.global_sleep_short)
            pag.press('enter')

        else:
            print("Проблема с идентификацией окна ГНГ!")
            globals.ExitByError()

    # else здесь нет, потому что если окно не появилось - мы ушли к следующей итерации расчёта