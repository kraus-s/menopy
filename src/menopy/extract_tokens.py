from menopy.menodoc import MeNoDoc
from bs4 import BeautifulSoup
from menopy.token import Token
from menopy.constants import LEMMATIZATION_RESOLVER_DICT
from menopy.constants import CLEANER_LIST
from menopy.constants import CHARACTER_RESOLVER_DICT

def reg_menota_parse(current_manuscript: MeNoDoc, soup: BeautifulSoup) -> MeNoDoc:
    res: list[Token] = []
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
            
            for k, v in LEMMATIZATION_RESOLVER_DICT.items():
                if lemming == k:
                    lemming = v
            if lemming == "?":
                lemming = "N/A"
        else:
            lemming = "N/A"
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
            token_parts_list_final.append(i.replace(" ", ""))
        currword = Token(normalized=token_parts_list_final[0], diplomatic=token_parts_list_final[1], facsimile=token_parts_list_final[2], lemma=token_parts_list_final[3], msa=msa_clean)
        current_manuscript.add_token(currword)
    return current_manuscript


def clean_tokens(tokens: list[Token]) -> list[Token]:
    res: list[Token] = []
    for tok in tokens:
        for k, v in LEMMATIZATION_RESOLVER_DICT.items():
                if tok.lemma == k:
                    tok.lemma = v
        tok.lemma = tok.lemma.strip()
        for char in CLEANER_LIST:
            tok.lemma = tok.lemma.replace(char, "")
        for k, v in CHARACTER_RESOLVER_DICT.items():
            tok.lemma = tok.lemma.replace(k, v)
            tok.normalized = tok.normalized.replace(k, v).strip()
            tok.diplomatic = tok.diplomatic.replace(k, v).strip()
            tok.facsimile = tok.facsimile.replace(k, v).strip()
        res.append(tok)
    return res	


def extract_tokens(soup: BeautifulSoup) -> list[Token]:
    res: list[Token] = []
    text_proper = soup.find_all('w')
    for word in text_proper:
        lemming = word.get('lemma')
        if lemming is not None:
            lemming = word.get('lemma')
        else:
            lemming = "N/A"
        facsimile_raw = word.find('me:facs')
        if facsimile_raw is not None:
            facsimile_clean = facsimile_raw.get_text()
        else:
            facsimile_clean = "N/A"
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
        res.append(Token(normalized=normalized_clean, diplomatic=diplomatic_clean, facsimile=facsimile_clean, lemma=lemming, msa=msa_clean))
        