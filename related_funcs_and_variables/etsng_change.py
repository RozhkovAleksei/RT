from loguru import logger

etsng_change = {
    "324116":	"324120",
    "351293":	"351289",
    "351306":	"351289",
    "351397":	"351382",
    "401026":	"401030",
    "401083":	"401098",
    "402103":	"402090",
    "411155":	"411140",
    "416137":	"416144",
    "462091":	"462087",
    "631131":	"631146",
    "631165":	"631150",
    "634089":	"634093",
    "641059":	"641044"}

@logger.catch(reraise=True)
def check_if_bad_etsng(etsng_code):
    if etsng_code in etsng_change.keys():
        print(f"Замена кода ЕТСНГ: {etsng_code} на {etsng_change[etsng_code]}")
        return etsng_change[etsng_code]
    return etsng_code
