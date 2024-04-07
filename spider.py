
import requests
from lxml import etree
import time
import random
import csv
import matplotlib.pyplot as plt

def get_data(city, page):
    url = f'https://{city}.lianjia.com/zufang/pg{page}/'
    headers_list = [
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'},
    ]
    headers = random.choice(headers_list)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html = response.text
        tree = etree.HTML(html)
        items = tree.xpath('//div[@class="content__list--item"]')
        data = []
        for item in items:
            # 提取房源信息
            title = item.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--title"]/a/text()')
            if title:
                title = title[0].strip()
            else:
                title = "N/A"

            description = item.xpath('.//div[@class="content__list--item--main"]/p[@class="content__list--item--des"]/text()')
            if description:
                description = description[0].strip()
            else:
                description = "N/A"

            price = item.xpath('.//div[@class="content__list--item--main"]/span[@class="content__list--item-price"]/em/text()')
            if price:
                price = price[0].strip()
                if '-' in price:  # 处理价格范围
                    price = price.split('-')[0]
            else:
                price = "N/A"

            # 将房源信息添加到数据列表中
            data.append([title, description, price])

            # 打印房源信息
            print(f'Title: {title}')
            print(f'Description: {description}')
            print(f'Price: {price}')
            print('---')

        # 设置随机间隔时间，防止请求过于频繁
        time.sleep(random.uniform(1, 3))
        return data
    else:
        print(f'Request failed. Status code: {response.status_code}')
        return []

def save_data(data):
    with open('rent_data.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Description', 'Price'])
        writer.writerows(data)

def plot_data(city):
    prices = []
    with open('rent_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过表头
        for row in reader:
            price = row[2]
            if price != "N/A":
                prices.append(int(price))

    # 绘制价格分布直方图
    plt.hist(prices, bins=30, edgecolor='k')
    plt.xlabel('Price')
    plt.ylabel('Count')
    plt.title(f'Rent Prices Distribution in {city}')
    plt.show()

def main():
    city = input("请输入要爬取的城市：")
    num_pages = int(input("请输入要爬取的页数："))

    all_data = []
    for page in range(1, num_pages + 1):
        data = get_data(city, page)
        all_data.extend(data)

    save_data(all_data)
    plot_data(city)

if __name__ == '__main__':
    main()
(f'Rent Prices Distribution in {city}')
    
