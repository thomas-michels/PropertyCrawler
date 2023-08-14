from bs4 import BeautifulSoup, Comment
from app.entities import RawProperty
import requests
import re


# url = "https://www.imoveisportal.com/busca/apartamento+loteterreno+casa+sobrado+geminada+loft/venda+locacao/blumenau"

# page_size = 16

# page = requests.get(url=url)

# with open("file.txt", "a") as file:
#     html = page.text
#     file.writelines(html)

with open("file.txt", "r") as file:
    html = file.read()

soup = BeautifulSoup(html, 'html.parser')

buttons = soup.find_all("a", class_="btn btn-primary")
properties = []

for button in buttons:
    # segundo callback
    print(button.attrs['href'])
    url = button.attrs['href']
    page = requests.get(url=url)
    html = page.text

    soup = BeautifulSoup(html, 'html.parser')

    if soup.title.next == "Página não encontrada":
        print("Imovel vendido ou alugado")
        continue

    image = soup.find("img", class_="thumb w-full lazy").attrs["data-src"]
    title = soup.find("h1", class_="title title-1 title-page").next
    room = soup.find("i", class_="fas fa-bed")

    if room:
        room = room.next.strip()

    else:
        room = 0

    bathroom = soup.find("i", class_="fas fa-bath")

    if bathroom:
        bathroom = bathroom.next.strip()

    else:
        bathroom = 0

    parking_space = soup.find("i", class_="fas fa-warehouse")

    if parking_space:
        parking_space = parking_space.next.strip()

    else:
        parking_space = 0

    size = soup.find("i", class_="fas fa-ruler")

    if size:
        size = size.next.strip()
        cleaned_size = re.sub(r'[^\d.]', '', size)

    else:
        cleaned_size = 0

    raw_type = re.search(r"/([^/]+)/([^/]+)", url)
    if raw_type:
        type = raw_type.group(2)
    else:
        type = "" 

    modality = soup.find("span", class_="type venda")
    code = soup.find("span", class_="type ref venda")

    if not modality:
        modality = soup.find("span", class_="type locacao").next
        code = soup.find("span", class_="type ref locacao").next

    else:
        modality = modality.next
        code = code.next

    description = soup.find("div", class_="col-lg-8 col-md-8 col-sm-7 col-xs-12")

    if description:
        description = description.text.strip()

    else:
        description = ""

    price = soup.find("span", "title title-2 price")

    if price:
        raw_price = price.next.strip()
        price = re.sub(r'[^\d,]', '', raw_price)
        price = float(price.replace(',', '.'))

    else:
        price = 0

    comments = soup.find_all(text=lambda text: isinstance(text, Comment))

    street = ""
    number = ""
    neighborhood = ""

    for comment in comments:
        formated = str(comment).lower()
        if formated.__contains__(" rua ") or formated.__contains__(" r "):
            street = formated
            neighborhood = comment.next.strip()

    if street:
        padrao_remover_r = r'^\s*r\s*(rua)?\s*'
        padrao_remover_hifen = r'\s*-\s*$'

        string = re.sub(padrao_remover_r, '', street, flags=re.IGNORECASE)
        string = re.sub(padrao_remover_hifen, '', string)

        street, number = re.split(r'\s*,\s*', string)
    
    properties.append(
        RawProperty(
            code=int(code),
            company="PORTAL_IMOVEIS",
            title=title,
            price=price,
            description=description,
            neighborhood=neighborhood,
            rooms=int(room),
            bathrooms=int(bathroom),
            size=float(cleaned_size),
            parking_space=int(parking_space),
            modality=modality,
            property_url=url,
            image_url=image,
            type=type,
            number=number,
            street=street
        )
    )

for i in properties:
    print(f"{i.model_dump()}")
    break
