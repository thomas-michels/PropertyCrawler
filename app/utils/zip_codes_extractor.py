from bs4 import BeautifulSoup
import requests
from time import sleep
from random import randint
from app.configs import get_logger
from unidecode import unidecode
import re

_logger = get_logger(__name__)
URL = "https://codigo-postal.org/pt-br/brasil/sc/blumenau/"
STREET_URL = "https://codigo-postal.org/pt-br/brasil/sc/blumenau/logradouro/$street/"

headers = {
    "domain": "https://codigo-postal.org/",
    "X-Domain": "https://codigo-postal.org/",
    "User-Agent": "PostmanRuntime/7.32.3"
}
url_pattern = r'href="([^"]*)"'

def extract_data(neighbor_url: str, streets_and_zip_codes: list = []):
    sleep(randint(1, 5))
    try:
        response = requests.request(method="GET", url=neighbor_url, headers=headers)

        response.raise_for_status()

    except Exception:
        return []

    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    raw_table = soup.find(id="tbody_results_")
    rows = list(raw_table.descendants)

    zip_code_rows = list(filter(lambda item: str(item).startswith("<tr"), rows))

    for row in zip_code_rows:
        text = row.text.strip().replace(" Blumenau/SC", "")

        zip_code = text[:9]

        text = text[10:]

        if len(text.split("  ")) > 1:
            street, _ = text.split("  ")
            
        else:
            try:
                index = text.index("(")

            except ValueError:
                index = text.index("-")

            if text[index - 1] != " ":
                new_index = text[index + 1:].index("-")
                street = text[index + new_index:]

            else:
                street = text[:index - 1]

        street = unidecode(street)

        if zip_code.lower() == "ver todos":
            search_street = street.lower().replace(" ", "-")
            print(search_street)
            
            new_street_url = STREET_URL.replace("$street", search_street)

            extract_data(neighbor_url=new_street_url, streets_and_zip_codes=streets_and_zip_codes)

        else:
            streets_and_zip_codes.append((street, zip_code))

    return streets_and_zip_codes


def save_ceps():
    _logger.info("Starting ZipCodes extractor")

    try:
        response = requests.request(method="GET", url=URL, headers=headers)

        response.raise_for_status()
        html = response.text

        soup = BeautifulSoup(html, "html.parser")

        raw_list = soup.find("ul", class_="column-list")
        neighborhoods = list(raw_list.descendants)
        only_li = list(filter(lambda item: str(item).startswith("<li>"), neighborhoods))
        all_streets_and_zip_codes = []

        with open("zip_codes.csv", "w") as file:
            for raw_neighborhood in only_li:
                neighbor_url = re.search(url_pattern, str(raw_neighborhood))
                neighbor_url = neighbor_url.group(1)

                neighbor_name = neighbor_url.split("/")[-2].replace("-", " ")
                neighbor_name = unidecode(neighbor_name)

                print(neighbor_name)

                streets_and_zip_codes = extract_data(neighbor_url=neighbor_url, streets_and_zip_codes=[])
                                
                for street_and_zip_code in streets_and_zip_codes:
                    file.write(f"{street_and_zip_code[1]};{neighbor_name.capitalize()};{street_and_zip_code[0]}\n")

                all_streets_and_zip_codes.extend(streets_and_zip_codes)

        print(all_streets_and_zip_codes)

    except Exception as error:
        _logger.error(f"Error: {str(error)}")

    _logger.info("Finishing extractor")

save_ceps()
