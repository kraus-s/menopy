from menopy.menodoc import MeNoDoc
from bs4 import BeautifulSoup
from menopy.token import Token
from menopy.constants import LEMMATIZATION_RESOLVER_DICT
from menopy.constants import CLEANER_LIST
from menopy.constants import CHARACTER_RESOLVER_DICT


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
        lemming = word.get('lemma', "N/A")
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
    return res


def token_extractor(soup: BeautifulSoup) -> list[Token]:
    tokens = extract_tokens(soup)
    cleaned_tokens = clean_tokens(tokens)
    return cleaned_tokens