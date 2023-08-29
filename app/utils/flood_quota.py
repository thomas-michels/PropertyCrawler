from bs4 import BeautifulSoup
from unidecode import unidecode


def save_flood_quota():
    streets = {}
    with open("zip_codes_coordinates.csv", "r") as file:
        lines = file.readlines()

        for line in lines:
            # 89041-470;Agua verde;Rua Acrisio Moreira da Costa;-26.9131994;-49.1156834
            data = line.split(";")
            street = data[2]
            street = street.replace("Rua ", "")
            street = street.replace("R ", "")
            streets[street.lower()] = {
                "complete_line": data
            }

    with open("CotasEnchentes.html", "r") as html:
        with open("flood_quota.csv", "w") as flood_file:
            with open("flood_quota_errors.csv", "w") as flood_error_file:
                soup = BeautifulSoup(html.read(), "html.parser")

                raw_table = soup.find('table', {"id": "tabela_cotas"})

                for row in raw_table.find_all("tr"):
                    row_data = []
                    for cell in row.find_all('td'):
                        row_data.append(cell.text)

                    if row_data:
                        street = row_data[0]
                        street = street.replace("Rua ", "")
                        street = street.replace("R ", "")

                        flood_quota = row_data[2].replace(",", ".")
                        flood_quota = float(flood_quota)

                        if streets.get(street.lower()):
                            completed_line = streets[street.lower()]["complete_line"]
                            completed_line = ';'.join(completed_line)
                            new_line = f"{completed_line.strip()};{flood_quota}\n"

                            flood_file.write(new_line)

                        else:
                            flood_error_file.write(f"{street};{flood_quota}\n")

save_flood_quota()
