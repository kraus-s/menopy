from bs4 import BeautifulSoup
import bs4
from menopy.constants import MENOTA_ENTITIES_URL
from menopy.token import Token
from menopy.menodoc import MeNoDoc
from menopy.load_menoxml import load_menoxml
from menopy.head_extractor import extract_head



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
        currword = Token(normalized=token_parts_list_final[0], diplomatic=token_parts_list_final[1], facsimile=token_parts_list_final[2], lemma=token_parts_list_final[3], msa=msa_clean)
        current_manuscript.add_token(currword)
    return current_manuscript


def parse(input_file: str) -> MeNoDoc:
    print("Parsing file...")
    soup = load_menoxml(input_file)
    current_manuscript = extract_head(soup)
    current_manuscript = reg_menota_parse(soup=soup, current_manuscript=current_manuscript)
    return current_manuscript


if __name__ == "__main__":
    test_stuff = parse("data/training/AM-519a-4to.xml")