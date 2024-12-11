from menopy.constants import MENOTA_ENTITIES_URL
import requests
import re
from bs4 import BeautifulSoup


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


def resolve_menota_entities(text: str, entity_mappings: dict[str, str]) -> str:
    for entity, unicode_char in entity_mappings.items():
        text = text.replace(entity, unicode_char)
    return text


def open_xml_file(tei_file: str, entity_mappings: dict[str, str]) -> BeautifulSoup:
    with open(tei_file, 'r', encoding='utf-8') as file:
        xml_content = file.read()
        xml_content = resolve_menota_entities(xml_content, entity_mappings)
        soup = BeautifulSoup(xml_content, from_encoding='UTF-8', features='lxml-xml')
    return soup


def load_menoxml(input_file: str) -> BeautifulSoup:
    entity_dict = download_and_parse_entities(MENOTA_ENTITIES_URL)
    return open_xml_file(input_file, entity_dict)