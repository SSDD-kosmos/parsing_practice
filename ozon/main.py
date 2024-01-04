import re
import json
import requests
import pandas as pd
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup as bs4
from bs4.element import Tag

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 '
                  'Safari/537.36',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Ch-Ua-Platform': "Windows",
    'Sec-Fetch-Mode': 'cors',
    'Sec-Ch-Ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"'
}

cookies = [
    {
        "name": "__cf_bm",
        "value": "aN8gbo3FaoDj1YoC2967QUvcBq7y.ztNwkaIfEG0rNU-1702408502-1"
                 "-Abz6VRwOh4XOQssgXhJrMXDjj7cI3QtM7VDBi5867C8EaWBubBTZtrZLG6tNOd5dBWU0tP7X3ta05NjfZ/qXRbg=",
        "domain": '.ozon.ru',
    },
    {
        "name": "__Secure-ab-group",
        "value": "56",
        "domain": '.ozon.ru',
    },
    {
        "name": "__Secure-access-token",
        "value": "3.0.3ddWmYGJSPm5KSfJADsP9w.56.l8cMBQAAAABj6Q44OTSZwqN3ZWKgAICQoA..20231212205513"
                 ".XFQ3jjCADAVyeo5KLrMJcr4TkhIYWfNyBleHB8NScv4",
        "domain": '.ozon.ru',
    },
    {
        "name": "__Secure-ext_xcid",
        "value": "24770345028da5a0890f5bf631a100d2",
        "domain": '.ozon.ru',
    },
    {
        "name": "__Secure-refresh-token",
        "value": "3.0.3ddWmYGJSPm5KSfJADsP9w.56.l8cMBQAAAABj6Q44OTSZwqN3ZWKgAICQoA..20231212205513"
                 ".3ji4DTjuC1kgqcMjfEyz2z_zp3nYHtPfSy8Djbqh5Xs",
        "domain": '.ozon.ru',
    },
    {
        "name": "__Secure-user-id",
        "value": "0",
        "domain": '.ozon.ru',
    },
    {
        "name": "ADDRESSBOOKBAR_WEB_CLARIFICATION",
        "value": "1702208903",
        "domain": 'www.ozon.ru',
    },
    {
        "name": "guest",
        "value": "true",
        "domain": 'www.ozon.ru',
    },
    {
        "name": "is_cookies_accepted",
        "value": "1",
        "domain": 'www.ozon.ru',
    },
    {
        "name": "rfuid",
        "value": "NjkyNDcyNDUyLDEyNC4wNDM0NzY1NzgwODEwMywxMzQ3MDc1MTIzLC0xLDI5MjAxMjI0NCxXM3NpYm1GdFpTSTZJbEJFUmlCV2FXVjNaWElpTENKa1pYTmpjbWx3ZEdsdmJpSTZJbEJ2Y25SaFlteGxJRVJ2WTNWdFpXNTBJRVp2Y20xaGRDSXNJbTFwYldWVWVYQmxjeUk2VzNzaWRIbHdaU0k2SW1Gd2NHeHBZMkYwYVc5dUwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjBzZXlKMGVYQmxJam9pZEdWNGRDOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5WFgwc2V5SnVZVzFsSWpvaVEyaHliMjFsSUZCRVJpQldhV1YzWlhJaUxDSmtaWE5qY21sd2RHbHZiaUk2SWxCdmNuUmhZbXhsSUVSdlkzVnRaVzUwSUVadmNtMWhkQ0lzSW0xcGJXVlVlWEJsY3lJNlczc2lkSGx3WlNJNkltRndjR3hwWTJGMGFXOXVMM0JrWmlJc0luTjFabVpwZUdWeklqb2ljR1JtSW4wc2V5SjBlWEJsSWpvaWRHVjRkQzl3WkdZaUxDSnpkV1ptYVhobGN5STZJbkJrWmlKOVhYMHNleUp1WVcxbElqb2lRMmh5YjIxcGRXMGdVRVJHSUZacFpYZGxjaUlzSW1SbGMyTnlhWEIwYVc5dUlqb2lVRzl5ZEdGaWJHVWdSRzlqZFcxbGJuUWdSbTl5YldGMElpd2liV2x0WlZSNWNHVnpJanBiZXlKMGVYQmxJam9pWVhCd2JHbGpZWFJwYjI0dmNHUm1JaXdpYzNWbVptbDRaWE1pT2lKd1pHWWlmU3g3SW5SNWNHVWlPaUowWlhoMEwzQmtaaUlzSW5OMVptWnBlR1Z6SWpvaWNHUm1JbjFkZlN4N0ltNWhiV1VpT2lKTmFXTnliM052Wm5RZ1JXUm5aU0JRUkVZZ1ZtbGxkMlZ5SWl3aVpHVnpZM0pwY0hScGIyNGlPaUpRYjNKMFlXSnNaU0JFYjJOMWJXVnVkQ0JHYjNKdFlYUWlMQ0p0YVcxbFZIbHdaWE1pT2x0N0luUjVjR1VpT2lKaGNIQnNhV05oZEdsdmJpOXdaR1lpTENKemRXWm1hWGhsY3lJNkluQmtaaUo5TEhzaWRIbHdaU0k2SW5SbGVIUXZjR1JtSWl3aWMzVm1abWw0WlhNaU9pSndaR1lpZlYxOUxIc2libUZ0WlNJNklsZGxZa3RwZENCaWRXbHNkQzFwYmlCUVJFWWlMQ0prWlhOamNtbHdkR2x2YmlJNklsQnZjblJoWW14bElFUnZZM1Z0Wlc1MElFWnZjbTFoZENJc0ltMXBiV1ZVZVhCbGN5STZXM3NpZEhsd1pTSTZJbUZ3Y0d4cFkyRjBhVzl1TDNCa1ppSXNJbk4xWm1acGVHVnpJam9pY0dSbUluMHNleUowZVhCbElqb2lkR1Y0ZEM5d1pHWWlMQ0p6ZFdabWFYaGxjeUk2SW5Ca1ppSjlYWDFkLFd5SnlkU0pkLDAsMSwwLDI0LDIzNzQxNTkzMCw4LDIyNzEyNjUyMCwwLDEsMCwtNDkxMjc1NTIzLFIyOXZaMnhsSUVsdVl5NGdUbVYwYzJOaGNHVWdSMlZqYTI4Z1RXRmpTVzUwWld3Z05TNHdJQ2hOWVdOcGJuUnZjMmc3SUVsdWRHVnNJRTFoWXlCUFV5QllJREV3WHpFMVh6Y3BJRUZ3Y0d4bFYyVmlTMmwwTHpVek55NHpOaUFvUzBoVVRVd3NJR3hwYTJVZ1IyVmphMjhwSUVOb2NtOXRaUzh4TWpBdU1DNHdMakFnVTJGbVlYSnBMelV6Tnk0ek5pQXlNREF6TURFd055Qk5iM3BwYkd4aCxleUpqYUhKdmJXVWlPbnNpWVhCd0lqcDdJbWx6U1c1emRHRnNiR1ZrSWpwbVlXeHpaU3dpU1c1emRHRnNiRk4wWVhSbElqcDdJa1JKVTBGQ1RFVkVJam9pWkdsellXSnNaV1FpTENKSlRsTlVRVXhNUlVRaU9pSnBibk4wWVd4c1pXUWlMQ0pPVDFSZlNVNVRWRUZNVEVWRUlqb2libTkwWDJsdWMzUmhiR3hsWkNKOUxDSlNkVzV1YVc1blUzUmhkR1VpT25zaVEwRk9UazlVWDFKVlRpSTZJbU5oYm01dmRGOXlkVzRpTENKU1JVRkVXVjlVVDE5U1ZVNGlPaUp5WldGa2VWOTBiMTl5ZFc0aUxDSlNWVTVPU1U1SElqb2ljblZ1Ym1sdVp5SjlmWDE5LDY1LC0xMjg1NTUxMywxLDEsLTEsMTY5OTk1NDg4NywxNjk5OTU0ODg3LDMzNjAwNzkzMyw4",
        "domain": '.ozon.ru',
    },
    {
        "name": "xcid",
        "value": "41285fa5ea5ec623071be99db8aa6ec0",
        "domain": 'www.ozon.ru',
    },
]


captured_data = []
search = '3070'

url = (f"https://www.ozon.ru/category/videokarty-i-karty-videozahvata-15720/?category_was_predicted=true"
       f"&deny_category_prediction=true&from_global=true&text={search}")

response = requests.get(url, headers=headers)

# chrome_options = ChromeOptions()
firefox_options = FirefoxOptions()

# chrome_options.add_argument("--headless=new")
firefox_options.add_argument("-headless")

# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Firefox(options=firefox_options)
driver.get(url)


def pageOpen(url):
    driver.delete_all_cookies()
    for cookie in cookies:
        driver.add_cookie(cookies[0])
        driver.add_cookie(cookies[1])
        driver.add_cookie(cookies[2])
        driver.add_cookie(cookies[4])
    driver.get(url)

    try:
        # ждем пока не появится на странице тэг с id ozonTagManagerApp
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ozonTagManagerApp"))
        )
    finally:
        # возвращаем текст страницы
        return driver.page_source


def options_dictionary(options_list: list) -> dict:
    options_dict = {}
    for option in options_list:
        options_dict[option.split(':')[0].strip()] = option.split(':')[1].strip()
    return options_dict


def images_dict(good_id: int, mask: str):
    images_dictionary = []
    try:
        # ищем div у которого в атрибуте data-state есть название имени файла
        data = soup.select_one(f'div[data-state*="{mask}"]')['data-state']
        # данные представлены в json формате, так что используем это и преобразуем в словарь
        json_data = json.loads(data)
        for link in json_data['items'][good_id]['tileImage']['items']:
            images_dictionary.append(link['image']['link'])
        return images_dictionary
    except:
        return []


def func_parse(items):
    idx = 0
    for sibling in items:
        if isinstance(sibling, Tag) and sibling.text:
            # создаем словарь, куда будем помещать все полученные данные для товара
            item = {}
            bonuses = False
            # если есть бонусы за товар, получаем их
            if t := sibling.div.next_sibling.next_sibling.select_one('div span > span b'):
                print(t.text)
                item['bonuses'] = t.text
                bonuses = True
            # получаем название товара
            print(item_name := sibling.div.next_sibling.next_sibling.div.a.span.span.text)
            item['name'] = item_name
            # получаем основную картинку предпросмотра
            img = sibling.div.a.div.div.img['src']
            item['preimage'] = img

            print(item_images := images_dict(idx, img.split('/')[-1]))
            item['images'] = item_images

            # если бонусы были, то смещаемся на один таг span
            n_child = 3 if bonuses else 2

            # вы таскиваем все options для товара
            if options := sibling.div.next_sibling.next_sibling.select_one(f'div > span:nth-child({n_child}) span'):
                options_str = str(options)
                # вырезаем ненужные тэги
                cleaned_str = re.sub(r'<?.span>|<font color="#......">|</font>', '', options_str)
                print(item_options := options_dictionary(cleaned_str.split('<br/>')))
                item['options'] = item_options
            idx += 1

            # в месте цены, html фрмируется по разному - обходим эти два варианта
            if price := sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.div.div:
                print((price_text := price.text[:-1].replace(' ', '')))
                # цена идет в кодировке, которая нам не подходит, возвращаем к человеческому виду
                item['price'] = int(price_text.encode('ascii', 'ignore'))
                # item['price'] = price_text
            elif price := sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.div.span.span:
                print((price_text := price.text[:-1].replace(' ', '')))
                item['price'] = int(price_text.encode('ascii', 'ignore'))
                # item['price'] = price_text

            # добавляем наш товар в список товаров
            captured_data.append(item)


for page in range(1, 3):
    # добавляем нужную страницу к url и отправляем в функцию pageOpen на скачку
    source_text = pageOpen(f'{url}&page={page}')
    # Удаляем из текста всякие комментарии
    result = re.sub(r'<!.*?->', '', source_text)
    soup = bs4(source_text, 'lxml')
    # данные о товарах
    items_body = (soup.find('div', id='paginatorContent').find('div', class_='widget-search-result-container')
                  .find('div', class_='x7i'))
    func_parse(items=items_body)

driver.quit()

df = pd.DataFrame(captured_data)
options_set = set()
# получаем уникальные названия опций
for i in captured_data:
    options_set = set(i['options'].keys()) | options_set

#  создаем новые колонки согласно опциям
for col in options_set:
    df[col] = np.nan


def options_parser(row):
    for option in options_set:
        row[option] = (row['options'].get(option))
    return row


df = df.apply(options_parser, axis=1)
df = df.drop(columns=['options'])
df.head(3)
df.to_excel('ozon_parse.xlsx')
