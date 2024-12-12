from bs4 import BeautifulSoup
import bs4
from menopy.constants import MENOTA_ENTITIES_URL
from menopy.menodoc import MeNoDoc
from menopy.load_menoxml import load_menoxml
from menopy.head_extractor import extract_head
from menopy.extract_tokens import token_extractor


def parse(input_file: str) -> MeNoDoc:
    print("Parsing file...")
    soup = load_menoxml(input_file)
    current_manuscript = extract_head(soup)
    tokens = token_extractor(soup)
    current_manuscript.tokens = tokens
    return current_manuscript


if __name__ == "__main__":
    test_stuff = parse("data/training/AM-519a-4to.xml")