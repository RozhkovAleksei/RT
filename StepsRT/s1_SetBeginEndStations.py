import pyautogui as pag
from time import sleep
from loguru import  logger
from RelatedFunctionsAndVariables import globals as gl
from RelatedFunctionsAndVariables.externals import sleep_short, sleep_long

@logger.catch(reraise=True)
def set_begin_end_stations(mobj):

    # Вызов функции, делающей активным окно с программой RT и передающей для комбинации из горячих клавиш
    # Номер вызываемого окна в качестве аргумента функции (Ctrl+1,2 и т.д.)
    gl.SetRailTariffWindowActiveForInput(1)

    sleep(sleep_short)

    if mobj.esr_otpr == '#Н/Д':
        gl.ExitByError()
    else:
        sleep(sleep_long)
        pag.typewrite(mobj.esr_otpr, interval=0.05)
        sleep(sleep_long)
        pag.press('enter')
        sleep(sleep_short)
        # wnd = win32gui.FindWindow(None, "Станция отправления")
        # if wnd != 0:
        #     mobj.is_ESR_correct = 0
        #     print("Проблема со станцией отправления")
        #     gl.ExitByError()

    sleep(sleep_short)

    gl.SetRailTariffWindowActiveForInput(2)

    sleep(sleep_short)

    # Вставляется код станции НАЗНАЧЕНИЯ, чтобы по фильтру ниже в окне появилось её название
    if mobj.esr_nazn == '#Н/Д':
        gl.ExitByError()
    else:
        sleep(sleep_long)
        pag.typewrite(mobj.esr_nazn, interval=0.05)
        sleep(sleep_long)
        pag.press('enter')
        sleep(sleep_short)
        # wnd = win32gui.FindWindow(None, "Станция назначения")
        # if wnd != 0:
        #     mobj.is_ESR_correct = 0
        #     print("Проблема со станцией назначения")
        #     gl.ExitByError()

    sleep(sleep_short)

