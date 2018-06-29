import json

import requests
from lxml import etree
import re
import time


class jdbooks(object):
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'
        }
        self.urls = [
            'https://list.jd.com/list.html?cat=1713,3287,3804&page={}&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main'.format(
                i) for i in range(0, 1)]
        self.price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}&pduid=1529748008301614117965'
        self.f = open('jd.txt', 'w')

    def send_request(self, url):
        return requests.get(url, headers=self.headers).content

    def parse(self, response):
        element = etree.HTML(response)
        title = element.xpath("//li[@class='gl-item']//div[@class='p-name']/a/em/text()")
        link = element.xpath("//li[@class='gl-item']//div[@class='p-name']/a/@href")
        publish = element.xpath(
            "//li[@class='gl-item']//div[@class='p-bookdetails']//span[@class='p-bi-store']/a/text()")
        author = element.xpath("//li[@class='gl-item']//div[@class='p-bookdetails']//span[@class='author_type_1']/a[1]/text()")
        for title, link, publish, author in zip(title, link, publish, author):
            item = dict()
            print(title)
            print(link)
            print(publish)
            print(author)
            sku_id = re.search(r'\d+', link).group()
            print(sku_id)
            js_str = self.send_request(self.price_url.format(sku_id)).decode('utf-8')
            print(js_str)
            price = eval(js_str)[0]['p']
            item['title'] = title.strip()
            item['price'] = price
            item['p_store'] = publish
            item['author'] = author
            self.save_file(item)

    def save_file(self, item):
        item = json.dumps(item)
        self.f.write(item + '\n')

    def run(self):
        for url in self.urls:
            response = self.send_request(url)
            self.parse(response)

        self.f.close()


if __name__ == '__main__':
    spider = jdbooks()
    start = time.time()
    spider.run()
    end = time.time()
    print('cost:{}s'.format(end - start))
