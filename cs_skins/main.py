from fake_useragent import UserAgent
import requests
import json

ua = UserAgent()


# print(ua.random)


def collect_data(weapon_type=4):
    offset = 0
    limit = 60
    result = []
    count = 0

    while True:
        for item in range(offset, offset + limit, 60):

            url = (f'https://cs.money/1.0/market/sell-orders?limit=60&maxPrice=10000&minPrice=3000&offset={offset}'
                   f'&type={weapon_type}')
            response = requests.get(
                url=url,
                headers={'user-agent': f'{ua.random}'}
            )

            offset += limit

            data = response.json()

            if data.get('error') == 2:
                return 'Data were collected'

            items = data.get('items')

            for i in items:

                if i.get('pricing').get('discount') > 0.25:
                    item_full_name = i.get('asset').get('names').get('full')
                    item_3d = i.get('links').get('3d')
                    item_discount = i.get('pricing').get('discount') * 100
                    item_price = i.get('pricing').get('computed')

                    result.append(
                        {
                            'full_name': item_full_name,
                            'item_3d': item_3d,
                            'item_discount': f'-{item_discount}',
                            'item_price': item_price
                        }
                    )

        count += 1
        print(f'Page #{count}')
        print(url)

        with open('result.json', 'w') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        print(len(result))


def main():
    print(collect_data(weapon_type=4))


if __name__ == '__main__':
    main()
