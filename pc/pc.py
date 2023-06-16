# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 22:18:13 2023

@author: HUAWEI
"""

import requests
from lxml import etree
import csv
import time


class DoubanSpider(object):
    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        }

    # 发请求 获响应
    def get_source(self, com_url):
        res = requests.get(com_url, headers=self.header)
        html = res.content.decode('utf-8')
        return html

    # 解析数据
    def parsed_source(self, html):
        tree = etree.HTML(html)
        divs = tree.xpath('//div[@class="info"]')
        # print(divs)
        lis_data = []
        for div in divs:
            d = {}
            # 标题
            title = div.xpath('./div[@class="hd"]/a/span/text()')[0].strip()
            # print(title)
            # 评分
            score = div.xpath('./div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0].strip()
            # print(score)
            # 评价人数
            evaluate = div.xpath('./div[@class="bd"]/div[@class="star"]/span[last()]/text()')[0].strip()
            # print(evaluate)
            # 引用
            quote = div.xpath('./div[@class="bd"]/p[@class="quote"]/span/text()')
            if quote:
                quote = quote[0]
            else:
                quote = ''
            # 电影链接url
            link_url = div.xpath('./div[@class="hd"]/a/@href')[0].strip()
            # print(link_url)
            # 根据key值提取数据
            d['title'] = title
            d['score'] = score
            d['evaluate'] = evaluate
            d['quote'] = quote
            d['link_url'] = link_url
            lis_data.append(d)
        # print(lis_data)
        return lis_data

    # 保存数据
    def save_source(self, move_data, header):
        with open('movie_data.csv', 'a', encoding='utf-8-sig', newline='') as f:
            w = csv.DictWriter(f, header)
            # 写入表头
            w.writeheader()
            # writerows 一次性写入多行数据
            w.writerows(move_data)

    # 主函数
    def main(self):
       