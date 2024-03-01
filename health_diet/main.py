import time
import requests
from bs4 import BeautifulSoup
import json
import csv

from fake_useragent import UserAgent


ua = UserAgent()

url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
headers = {
    'Accept': '*/*',
    'User-Agent': f'{ua.random}',
}


def update_links():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')

    all_categories_dict = {}

    for item in all_products_hrefs:
        item_text = item.text
        item_href = 'https://health-diet.ru' + item.get('href')

        all_categories_dict[item_text] = item_href

    with open('all_categories_dict.json', 'w') as file:
        json.dump(all_categories_dict, file, indent=4, ensure_ascii=False)

    return all_categories_dict


class CategoriesLoader:
    def __init__(self, file_name=None):
        self.file_name = file_name
        self.all_categories = None

    def __enter__(self):
        with open(self.file_name) as file:
            self.all_categories = json.load(file)
        return self.all_categories

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"An error occurred: {exc_type}, {exc_value}")
        else:
            print("Categories loaded successfully")
        return False


class ProductParameters(CategoriesLoader):
    def __init__(self, file_name=None, count=0):
        super().__init__(file_name)
        self.count = count

    def data_collection(self):
        with CategoriesLoader('all_categories_dict.json') as file:
            all_categories = file

        iteration_count = int(len(all_categories)) - 1
        print(f'Всего категорий: {iteration_count}')

        for category_name, category_href in all_categories.items():
            rep = [",", " ", "-", "'"]
            for i in rep:
                if i in category_name:
                    category_name = category_name.replace(i, '_')

            req = requests.get(url=category_href, headers=headers)
            src = req.text

            with open(f'data/{self.count}_{category_name}.html', 'w') as file:
                file.write(src)

            with open(f'data/{self.count}_{category_name}.html') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')

            # Проверка страницы на наличие таблицы с продуктами
            alert_block = soup.find(class_='uk-alert-danger')
            if alert_block is not None:
                continue

            # Собираем заголовки
            table_head = soup.find(class_='mzr-tc-group-table').find('tr').find_all('th')
            product = table_head[0].text
            calories = table_head[1].text
            proteins = table_head[2].text
            fats = table_head[3].text
            carbohydrates = table_head[4].text

            with open(f'data/{self.count}_{category_name}.csv', 'w', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        product,
                        calories,
                        proteins,
                        fats,
                        carbohydrates,
                    )
                )

            # Соберем данные продуктов
            products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')

            product_info = []

            for item in products_data:
                product_tds = item.find_all('td')

                title = product_tds[0].find('a').text
                calories = product_tds[1].text
                proteins = product_tds[2].text
                fats = product_tds[3].text
                carbohydrates = product_tds[4].text

                product_info.append(
                    {
                        'Title': title,
                        'Calories': calories,
                        'Proteins': proteins,
                        'Fats': fats,
                        'Carbohydrates': carbohydrates,
                    }
                )

                with open(f'data/{self.count}_{category_name}.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        (
                            title,
                            calories,
                            proteins,
                            fats,
                            carbohydrates,
                        )
                    )

            with open(f'data/{self.count}_{category_name}.json', 'a', encoding='utf-8') as file:
                json.dump(product_info, file, indent=4, ensure_ascii=False)

            self.count += 1

            print(f'# Итерация {self.count}. {category_name} записан...')
            iteration_count = iteration_count - 1

            if iteration_count == 0:
                print('Работа завершена')
                break

            print(f'Осталось итераций: {iteration_count}')
            time.sleep(2)





