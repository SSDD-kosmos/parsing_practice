# import datetime
# import requests
# import csv
# from fake_useragent import UserAgent
#
#
# def collect_data(city_code='1761'):
#     cur_time = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')
#     ua = UserAgent()
#
#     headers = {
#         # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
#         #           'application/signed-exchange;v=b3;q=0.7',
#         'User-Agent': ua.random,
#         'Accept': '*/*',
#         'Accept-Language': 'ru',
#         'Connection': 'keep-alive',
#         'Origin': 'https://magnit.ru',
#         'Referer': 'https://magnit.ru/',
#         'Sec-Fetch-Dest': 'empty',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Site': 'same-site',
#         'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
#         'sec-ch-ua-mobile': '?0',
#         'sec-ch-ua-platform': '"macOS"',
#         'x-app-version': '0.1.0',
#         'x-client-name': 'magnit',
#         'x-device-id': 'ld9kmkxpt2',
#         'x-device-platform': 'Web',
#         'x-device-tag': 'disabled',
#         'x-platform-version': 'window.navigator.userAgent',
#     }
#
#     cookies = {
#         'mg_geo_id': f'{city_code}'
#     }
#
#     params = {
#         'offset': '0',
#         'limit': '1000',
#         'storeId': '161433',
#         'sortBy': 'priority',
#         'order': 'desc',
#         'adult': 'true',
#     }
#
#     response = requests.get('https://web-gateway.middle-api.magnit.ru/v1/promotions', params=params, headers=headers)
#
#     with open(f'{cur_time}.csv', 'w') as file:
#         writer = csv.writer(file)
#
#         writer.writerow(
#             (
#                 'Продукт',
#                 'Старая цена',
#                 'Новая цена',
#                 'Процент скидки',
#                 'Время акции',
#             )
#         )
#
#     data = response.json()['data']
#
#     for d in data:
#         d_name = d.get('name').strip()
#
#         try:
#             d_discount = d.get('discountLabel')
#         except AttributeError:
#             continue
#
#         try:
#             d_old_price = d.get('oldPrice')/100
#         except TypeError:
#             continue
#
#         try:
#             d_new_price = d.get('price')/100
#         except TypeError:
#             continue
#
#         d_start_date = d.get('startDate')
#         d_end_date = d.get('endDate')
#         d_date = f'С {d_start_date} по {d_end_date}'
#
#         with open(f'{cur_time}.csv', 'a') as file:
#             writer = csv.writer(file)
#
#             writer.writerow(
#                 (
#                     d_name,
#                     d_old_price,
#                     d_new_price,
#                     d_discount,
#                     d_date,
#                 )
#             )
#
#     print(f'Файл Saint-Petersburg {cur_time} успешно создан!')
#
#
# def main():
#     collect_data(city_code='1761')
#
#
# if __name__ == '__main__':
#     main()
