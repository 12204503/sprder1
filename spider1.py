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
            else:
                price = "N/A"

            # 保存房源信息到CSV文件
            save_data(city, title, description, price)

            # 打印房源信息
            print(f'Title: {title}')
            print(f'Description: {description}')
            print(f'Price: {price}')
            print('---')

        # 设置随机间隔时间，防止请求过于频繁
        time.sleep(random.uniform(1, 3))
    else:
        print(f'Request failed. Status code: {response.status_code}')

def save_data(city, title, description, price):
    with open(f'{city}_rent_data.csv', 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([title, description, price])

def plot_data(city):
    prices = []
    with open(f'{city}_rent_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            price = row[2]
            prices.append(int(price))
    
    # 绘制价格分布直方图
    plt.hist(prices, bins=20, edgecolor='black')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    plt.title(f'Price Distribution in {city}')
    plt.show()

def main():

    city = input("请输入要爬取的城市名称（拼音）：")
    page_num = int(input("请输入要爬取的页数："))

    for page in range(1, page_num + 1):
        get_data(city, page)

    save_option = input("是否保存爬取的数据到CSV文件？(Y/N)：")
    if save_option.lower() == 'y':
        print("数据保存成功！")

    plot_option = input("是否绘制价格分布图？(Y/N)：")
    if plot_option.lower() == 'y':
        plot_data(city)

if __name__ == '__main__':
    main()
    
