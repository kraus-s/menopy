from bs4 import BeautifulSoup
import bs4
import requests
import re
from menota_parser.constants import MENOTA_ENTITIES_URL


class token:

    normalized: str
    diplomatic: str
    facsimile: str
    lemma: str
    msa: str

    def __init__(self,
                normalized: str,
                diplomatic: str,
                facsimile: str,
                lemma: str,
                msa: str) -> None:
        self.normalized = normalized
        self.diplomatic = diplomatic
        self.facsimile = facsimile
        self.lemma = lemma
        self.msa = msa


class sent:

    order: int
    tokens: list[token]

    def __init__(self, order: int) -> None:
        self.order = order
        self.tokens = []

    def add_token(self, newtoken: token):
        self.tokens.append(newtoken)


class MeNoDoc:

    name: str
    ms: str
    tokens: list[token]
    lemmatized: bool
    diplomatic: bool
    normalized: bool
    facsimile: bool
    msa: bool
    
    def __init__(self, name: str, manuscript: str, lemmatized: bool, diplomatic: bool, normalized: bool, facsimile: bool, msa: bool) -> None:
        self.name = name
        self.ms = manuscript
        self.sents = []
        self.tokens = []
        self.lemmatized = lemmatized
        self.diplomatic = diplomatic
        self.normalized = normalized
        self.facsimile = facsimile
        self.msa = msa
    
    def add_token(self, newtoken: token):
        self.tokens.append(newtoken)
    
    def get_full_text(self, level: str) -> str:
        full_text = ""
        for token in self.tokens:
            if level == "diplomatic":
                full_text += token.diplomatic + " "
            elif level == "normalized":
                full_text += token.normalized + " "
            elif level == "facsimile":
                full_text += token.facsimile + " "
            elif level == "lemma":
                full_text += token.lemma + " "
        return full_text


def download_and_parse_entities(url) -> dict[str, str]:
    """Retrieve and parse the MENOTA entity mapping file.
    Args:
        url: The URL of the MENOTA entity mapping file.
    Returns:
        dict: A mapping of entity names to unicode characters."""
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()

    entity_mappings = {}
    entity_declaration_pattern = re.compile(r'<!ENTITY\s+(\w+)\s+"&#x([0-9A-Fa-f]+);">')
    for line in lines:
        match = entity_declaration_pattern.search(line)
        if match:
            entity_name, unicode_hex = match.groups()
            entity = f'&{entity_name};'
            unicode_char = chr(int(unicode_hex, 16))
            entity_mappings[entity] = unicode_char
    return entity_mappings


def replace_entities(text, entity_mappings):
    for entity, unicode_char in entity_mappings.items():
        text = text.replace(entity, unicode_char)
    return text


def read_tei(tei_file: str, entity_mappings: dict[str, str]) -> BeautifulSoup:
    with open(tei_file, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        xml_content = replace_entities(xml_content, entity_mappings)
        soup = BeautifulSoup(xml_content, from_encoding='UTF-8', features='lxml-xml')
    return soup


def get_menota_info (soup: BeautifulSoup) -> MeNoDoc:
    try:
        ms_metadata = soup.find("sourcedesc")
        shelfmark_ = ms_metadata.find('idno')
        shelfmark = shelfmark_.get_text()
        txt_name_raw = ms_metadata.find("msname")
        txt_name = txt_name_raw.get_text()
    except:
        ms_metadata = soup.find("sourceDesc")
        shelfmark_ = ms_metadata.find('idno')
        shelfmark = shelfmark_.get_text()
        txt_name_raw = ms_metadata.find("msName")
        txt_name = txt_name_raw.get_text()
    try:
        levels = soup.find("normalization")
        levels = levels["me:level"]
        levels = levels.split()
    except:
        import pdb; pdb.set_trace()
    if "dipl" in levels:
        diplomatic = True
    else:
        diplomatic = False
    if "norm" in levels:
        normalized = True
    else:
        normalized = False
    if "facs" in levels:
        facsimile = True
    else:
        facsimile = False
    interpretations = soup.find("interpretation")
    if interpretations is not None:
        if interpretations["me:lemmatized"] == "completely":
            lemmatized = True
        else:
            lemmatized = False
        if interpretations["me:morphAnalyzed"] == "completely":
            msa = True
        else:   
            msa = False
    else:
        emroon = False
        for string in soup.strings:
            if "emroon" in string:
                emroon = True
        if emroon:
            msa = True
            lemmatized = True
        else:
            msa = False
            lemmatized = False
    
    current_manuscript = MeNoDoc(name=txt_name, manuscript=shelfmark, lemmatized=lemmatized, diplomatic=diplomatic, normalized=normalized, facsimile=facsimile, msa=msa)

    return current_manuscript


def reg_menota_parse(current_manuscript: MeNoDoc, soup: bs4.BeautifulSoup, for_nlp: bool = True) -> MeNoDoc:
    text_proper = soup.find_all('w')

    for word in text_proper:
        lemming = word.get('lemma')
        if lemming is not None:
            lemming = word.get('lemma')
            if "-" in lemming:
                lemming = lemming.replace("-", "")
            if "(" in lemming:
                lemming = lemming.replace("(", "")
            if ")" in lemming:
                lemming = lemming.replace(")", "")
            lemming = lemming.lower()

            # Sometimes there are some weird lemmatizations that need to be fixed manually. These have been checked against the ONP.
            weird_lemmatization_dict = {"kaupsskip": "kaupskip", "slǫngva": "sløngva", "þrøngva þrøngja": "þrøngva"}
            for k, v in weird_lemmatization_dict.items():
                if lemming == k:
                    lemming = v
            if lemming == "?":
                lemming = "-"
        else:
            lemming = "-"
        facsimile_raw = word.find('me:facs')
        if facsimile_raw is not None:
            facsimile_clean = facsimile_raw.get_text()
        else:
            facsimile_clean = "-"
        diplomatic_raw = word.find('me:dipl')
        if diplomatic_raw is not None:
            diplomatic_clean = diplomatic_raw.get_text()
        else:
            diplomatic_clean = "-"
        normalized_raw = word.find('me:norm')
        if normalized_raw is not None:
            normalized_clean = normalized_raw.get_text()
        else:
            normalized_clean = "-"
        msa_raw = word.get('me:msa')
        if msa_raw is not None:
            msa_clean = word.get('me:msa')
        else:
            msa_clean = "-"
        token_parts_list_final: list[str] = []

        # Sometimes the entity resolution does not work properly, so some manual replacements are necessary. This also includes some normalization of the text.
        for i in [normalized_clean, diplomatic_clean, facsimile_clean, lemming]:
            weird_chars_dict = {"ҩoogon;": "ǫ", "ҩoslashacute;": "ǿ", "ҩaeligacute;": "ǽ", "lͣ": "l", "io": "jo", "ió": "jó", "ia": "ja"}
            for k, v in weird_chars_dict.items():
                if k in i:
                    i = i.replace(k, v)
            if for_nlp:
                i = i.lower()
            token_parts_list_final.append(i.replace(" ", ""))
        currword = token(normalized=token_parts_list_final[0], diplomatic=token_parts_list_final[1], facsimile=token_parts_list_final[2], lemma=token_parts_list_final[3], msa=msa_clean)
        current_manuscript.add_token(currword)
    return current_manuscript


def get_regular_text(input_file: str) -> MeNoDoc:
    print("Parsing regular text...")
    entity_dict = download_and_parse_entities(MENOTA_ENTITIES_URL)
    soup = read_tei(input_file, entity_dict)
    current_manuscript = get_menota_info(soup)
    current_manuscript = reg_menota_parse(soup=soup, current_manuscript=current_manuscript)
    return current_manuscript


if __name__ == "__main__":
    test_stuff = get_regular_text("data/training/AM-519a-4to.xml")