MENOTA_ENTITIES_URL = "http://www.menota.org/menota-entities.txt"

LEMMATIZATION_RESOLVER_DICT = {
    "kaupsskip": "kaupskip",
    "slǫngva": "sløngva",
    "þrøngva þrøngja": "þrøngva"
    }

CLEANER_LIST = ["(", ")", "-"]

CHARACTER_RESOLVER_DICT = weird_chars_dict = {
    "ҩoogon;": "ǫ",
    "ҩoslashacute;": "ǿ",
    "ҩaeligacute;": "ǽ",
    "lͣ": "l",
    "io": "jo",
    "ió": "jó",
    "ia": "ja"
    }