from geopy.geocoders import Nominatim
from time import sleep

geolocator = Nominatim(user_agent="PropertyCrawler")
location = geolocator.geocode(query={"street": "Rua Erwin Henschel", "country": "brazil"})
print(location.address)

print((location.latitude, location.longitude))
