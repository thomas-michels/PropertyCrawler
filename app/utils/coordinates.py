from geopy.geocoders import Nominatim
import csv
from time import sleep

def save_coordinates():
    geolocator = Nominatim(user_agent="PropertyCrawler")

    with open("zip_codes.csv", "r") as file:
        reader = csv.reader(file, delimiter=";")
        country = "Brazil"
        city = "Blumenau"

        with open("zip_code_errors.csv", "w") as error_file:
            with open("zip_codes_coordinates.csv", "w") as file_write:
                for i, row in enumerate(reader):
                    try:
                        sleep(2)
                        print(f"{i} de 4643")
                        location = geolocator.geocode(query={
                            "street": row[2],
                            "city": city,
                            "country": country
                        })

                        if location:
                            print((location.latitude, location.longitude))
                            row.append(str(location.latitude))
                            row.append(str(location.longitude))
                            completed_row = ";".join(row) + "\n"
                            file_write.write(completed_row)

                        else:
                            error_file.write("; ".join(row) + "\n")

                    except Exception as error:
                        print(f"Error: {str(error)}")
                        error_file.write("; ".join(row) + "\n")

save_coordinates()
