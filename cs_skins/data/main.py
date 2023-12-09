from fake_useragent import UserAgent
import requests
import json

ua = UserAgent()


class Collection:

    def __init__(self, weapon_type, data_list=None):
        self.weapon_type = weapon_type
        self.data_list = data_list or []

    def collect_data(self, minPrice=5000, maxPrice=10000, discount=25):
        offset = 0
        limit = 60
        count = 0

        for item in range(offset, 120 + limit, 60):
            url = (f'https://cs.money/1.0/market/sell-orders?limit=60&maxPrice={maxPrice}'
                   f'&minPrice={minPrice}&offset={item}&type={self.weapon_type}')
            response = requests.get(
                url=url,
                headers={'user-agent': f'{ua.random}'}
            )

            offset += limit
            data = response.json()
            items = data.get('items', [])

            for i in items:

                if i.get('pricing', {}).get('discount') > int(discount)/100:
                    item_full_name = i.get('asset', {}).get('names', {}).get('full')
                    item_3d = i.get('links', {}).get('3d')
                    item_discount = i.get('pricing', {}).get('discount', 0) * 100
                    item_price = i.get('pricing', {}).get('computed')

                    self.data_list.append(
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
            print(len(self.data_list))

    def save(self):
        with open('result.json', 'w') as file:
            json.dump(self.data_list, file, indent=4, ensure_ascii=False)


def main():
    col = Collection(weapon_type=2)
    col.collect_data()
    col.save()


if __name__ == '__main__':
    main()
