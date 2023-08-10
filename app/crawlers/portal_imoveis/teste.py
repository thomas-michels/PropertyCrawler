from bs4 import BeautifulSoup
import requests

url = "https://www.imoveisportal.com/busca/apartamento+loteterreno+casa+sobrado+geminada+loft/venda+locacao/blumenau"

page_size = 16

page = requests.get(url=url)

with open("file.txt", "a") as file:
    html = page.text
    file.writelines(html)

print(html)
