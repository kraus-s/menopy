from bs4 import BeautifulSoup
from menopy.menodoc import MeNoDoc


def get_shelfmark_and_txtname(soup: BeautifulSoup) -> tuple[str, str, str]:
    """Extracts the shelfmark and the name of the text from the XML file."""
    # TODO: Better handling of case sensitivity
    try:
        ms_metadata = soup.find("sourcedesc")
        shelfmark_ = ms_metadata.find('idno')
        shelfmark = shelfmark_.get_text()
        txt_name_raw = ms_metadata.find("msname")
        txt_name = txt_name_raw.get_text()
    except AttributeError:
        # TODO: Implement proper error handling, at least some logging
        ms_metadata = soup.find("sourceDesc")
        shelfmark_ = ms_metadata.find('idno')
        shelfmark = shelfmark_.get_text()
        txt_name_raw = ms_metadata.find("msName")
        txt_name = txt_name_raw.get_text()
    return shelfmark, txt_name


def get_edition_levels(soup: BeautifulSoup) -> tuple[bool, bool, bool]:
    """Extracts the transcription levels from the XML file."""
    diplomatic, normalized, facsimile = _get_transcription_levels(soup)
    lemmatized, msa = _get_annotation_levels(soup)
    return diplomatic, normalized, facsimile, lemmatized, msa


def _get_transcription_levels(soup: BeautifulSoup) -> tuple[bool, bool, bool]:
    try:
        levels = soup.find("normalization")
        levels = levels["me:level"]
        levels = levels.split()
    except Exception as e:
        raise e
        # TODO: Implement proper error handling
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
    return diplomatic, normalized, facsimile


def _get_annotation_levels(soup: BeautifulSoup) -> tuple[bool, bool]:
    lemmatized = False
    msa = False
    interpretations = soup.find("interpretation")
    if interpretations is not None:
        if interpretations["me:lemmatized"] == "completely":
            lemmatized = True
        if interpretations["me:morphAnalyzed"] == "completely":
            msa = True
    else:
        for string in soup.strings:
            if "emroon" in string:
                msa = True
                lemmatized = True
    return lemmatized, msa


def extract_head(soup: BeautifulSoup) -> MeNoDoc:
    shelfmark, txt_name = get_shelfmark_and_txtname(soup)
    diplomatic, normalized, facsimile, lemmatized, msa = get_edition_levels(soup)
    return MeNoDoc(name=txt_name, manuscript=shelfmark, lemmatized=lemmatized, diplomatic=diplomatic, normalized=normalized, facsimile=facsimile, msa=msa)
