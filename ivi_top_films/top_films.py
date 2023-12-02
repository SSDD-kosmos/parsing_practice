import json
import requests
from bs4 import BeautifulSoup

data = []
url = 'https://www.ivi.ru/collections/best-movies?sort=pop'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
films = soup.findAll('li', class_='gallery__item')

for film in films:
    try:
        link = 'https://www.ivi.ru' + (film.find('a', class_='nbl-slimPosterBlock').get('href'))
    except AttributeError:
        link = None

    try:
        film_name = (film.find('a', class_='nbl-slimPosterBlock')
                     .find('span', class_='nbl-slimPosterBlock__titleText').text)
    except AttributeError:
        film_name = None

    try:
        first_number_rating = (film.find('a', class_='nbl-slimPosterBlock')
                               .find('div', class_='nbl-ratingCompact__valueInteger').text)
        second_number_rating = (film.find('a', class_='nbl-slimPosterBlock')
                                .find('div', class_='nbl-ratingCompact__valueFraction').text)
    except AttributeError:
        first_number_rating = None
        second_number_rating = None

    rating = first_number_rating + second_number_rating

    try:
        information_film = (film.find('a', class_='nbl-slimPosterBlock')
                            .findAll('div', class_='nbl-poster__propertiesRow')[1].text.split(','))
    except AttributeError:
        information_film = None

    country = information_film[1]
    film_type = information_film[2]

    data.append(
        {
            'Film link': link,
            'Name': film_name,
            'Rating': rating,
            'Country': country,
            'Film type': film_type
        }
    )

with open('top_films.json', 'a', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print('Готово')
