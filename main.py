import csv
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
from datetime import datetime

def get_html(url, city_code=2398):
    ua = UserAgent()

    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'User Agent': ua.random
    }

    cookies = {'mg_geo_id': f'{city_code}'}

    res = requests.get(url=url, headers=headers, cookies=cookies)

    return res.content


def main():
    url = 'https://magnit.ru/promo/'
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    cur_time = datetime.now().strftime('%d_%m_%Y_%H_%M')
    city_name = soup.find('span', class_='header__contacts-text').text.strip()
    cards = soup.find_all('a', class_='card-sale_catalogue')

    with open(f'{city_name}_{cur_time}.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        writer.writerow((
            'Название товара', 
            'Старая цена',
            'Новая цена',
            'Процент скидки',
            'Период проведения акции'
        ))
    
    for card in cards:
        try:
            card_discount = card.find('div', class_='card-sale__discount').text.strip()
        except:
            continue
        
        card_title = card.find('div', class_='card-sale__title').text.strip()
        
        card_old_price_integer = card.find('div', class_='label__price_old').find('span', class_='label__price-integer').text.strip()
        card_old_price_decimal = card.find('div', class_='label__price_old').find('span', class_='label__price-decimal').text.strip()
        card_old_price = f'{card_old_price_integer}.{card_old_price_decimal}'
        
        card_new_price_integer = card.find('div', class_='label__price_new').find('span', class_='label__price-integer').text.strip()
        card_new_price_decimal = card.find('div', class_='label__price_new').find('span', class_='label__price-decimal').text.strip()
        card_new_price = f'{card_new_price_integer}.{card_new_price_decimal}'
        
        card_sale_date = card.find('div', class_='card-sale__date').text.strip().replace('\n', ' ')
        
        with open(f'{city_name}_{cur_time}.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow((
                card_title,
                card_old_price,
                card_new_price,
                card_discount,
                card_sale_date
            ))
           
    
    


if __name__ == '__main__':
    main()