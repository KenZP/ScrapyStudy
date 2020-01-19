# -*- coding: utf-8 -*-
import scrapy
from stock_code import GetStockCodes
import json


class GupiaoSpider(scrapy.Spider):
    name = 'gupiao'
    allowed_domains = ['qd.10jqka.com.cn']
    # start_urls = ['http://stockpage.10jqka.com.cn/{0}/']
    urls = "http://qd.10jqka.com.cn/quote.php?cate=real&type=stock&return=json&callback=showStockData&code={0}"
    list_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
    }

    def start_requests(self):
        # time.sleep(3)
        get_stock_list = GetStockCodes()
        stock_codes = get_stock_list.get_stock_list()
        for code in stock_codes:
            yield scrapy.Request(url=self.urls.format(code), headers=self.list_headers, meta={'stock_code': code},
                                 callback=self.parse_code)
            # yield scrapy.Request(
            #     url=self.url,
            #     method='POST',
            #     body=form_data_json,
            #     headers=self.list_headers,
            #     callback=self.parse_page
            # )

    def parse_code(self, response):
        stock_dict = json.loads(response.text[14:int(len(response.text))-1])
        code = response.meta['stock_code']
        name = stock_dict['info'][code]['name']
        begin = stock_dict['data'][code]['7']
        pass
