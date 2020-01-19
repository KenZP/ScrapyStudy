# -*- coding: utf-8 -*-
import json
import os
import time

import scrapy
from myspider.items import BihuItemLoads, BihuspiderItem
import requests


class BihuSpider(scrapy.Spider):
    name = 'bihu'
    allowed_domains = ['bihu.com']
    url = 'https://be02.bihu.com/bihube-pc/api/content/show/hotArtList'
    article_url = 'https://be02.bihu.com/bihube-pc/api/content/show/getArticle2'
    list_headers = {
        'Host': 'be02.bihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json;charset=utf-8',
        'device': 'web',
        'version': '2.6.0',
        # 'nonce': 'a9fee1c8-e1d9-4799-8812-ce187a3acbb1',
        'timestamp': int(round(time.time() * 1000)),
        'uuid': 'a0ad8806edf9361d49d23475d5f88d05',
        # 'Content-Length': '37',
        'Origin': 'https://bihu.com',
        # 'Connection': 'keep-alive',
        'Referer': 'https://bihu.com/',
        'DNT': '1',
    }

    content_header = {
        'Host': 'oss02.bihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        # 'Content-Type': 'application/json;charset=utf-8',
        # 'Content-Length': '37',
        'Origin': 'https://bihu.com',
        # 'Connection': 'keep-alive',
        'Referer': 'https://bihu.com/',
        'DNT': '1',
    }

    detail_header = {
        'Host': 'be02.bihu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json;charset=utf-8',
        'device': 'web',
        'version': '2.6.0',
        # 'nonce': 'a9fee1c8-e1d9-4799-8812-ce187a3acbb1',
        'timestamp': int(round(time.time() * 1000)),
        'uuid': 'a0ad8806edf9361d49d23475d5f88d05',
        # 'Content-Length': '37',
        'Origin': 'https://bihu.com',
        # 'Connection': 'keep-alive',
        'Referer': 'https://bihu.com/',
        'DNT': '1',
    }

    formdata = {
        'pageNum': '1'
    }

    def start_requests(self):
        is_exist = os.path.exists('F:\Study\Python\ScrapyStudy\myspider\\article')
        if not is_exist:
            os.makedirs('F:\Study\Python\ScrapyStudy\myspider\\article')  # 创建一个存放文章的文件夹
        form_data_json = json.dumps(self.formdata)
        # time.sleep(3)
        yield scrapy.Request(
            url=self.url,
            method='POST',
            body=form_data_json,
            headers=self.list_headers,
            callback=self.parse_page
        )

    def parse_page(self, response):
        # print(response.text)
        datas = json.loads(response.body)
        page_number = datas['data']['pageNum']
        print(page_number)
        next_page = datas['data']['nextPage']
        have_next_page = datas['data']['hasNextPage']
        list_infos = datas['data']['list']
        for list_info in list_infos:
            # info = dict()
            article_id = int(list_info['id'])
            article_formdata = {
                'artId': article_id
            }
            article_formdata_json = json.dumps(article_formdata)
            self.detail_header['Referer'] = 'https://bihu.com/article/{0}'.format(article_id)
            yield scrapy.Request(url=self.article_url, method='POST', body=article_formdata_json,
                                 headers=self.detail_header, callback=self.parse_detail)

        if have_next_page:
            self.formdata['pageNum'] = next_page
            formdata_json = json.dumps(self.formdata)
            time.sleep(3)
            yield scrapy.Request(url=self.url, method='POST', body=formdata_json, headers=self.list_headers,
                                 callback=self.parse_page)

    def parse_detail(self, response):
        # print(response.text)
        article_datas = json.loads(response.body)
        article_id = article_datas['data']['id']
        author = article_datas['data']['userName']
        user_id = article_datas['data']['userId']
        money = article_datas['data']['money']
        ups = article_datas['data']['ups']
        comments = article_datas['data']['cmts']
        title = article_datas['data']['title']
        articledesc = article_datas['data']['snapContent']
        content_url = article_datas['data']['content']
        create_time_stamp = article_datas['data']['creatime']
        update_time_stamp = article_datas['data']['updatime']

        full_content_url = 'https://oss02.bihu.com/{0}'.format(content_url)
        self.content_header['Host'] = "oss02.bihu.com"
        self.content_header['Referer'] = 'https://bihu.com/article/{0}'.format(article_id)
        # time.sleep(2)
        article_response = requests.get(url=full_content_url, headers=self.content_header)
        contents = article_response.text.encode('ISO-8859-1').decode('utf8')
        # contents_file = article_response.text
        # os.makedirs('article')  # 创建一个存放文章的文件夹
        os.chdir('F:\Study\Python\ScrapyStudy\myspider\\article')  # 切换到上面创建的文件夹
        filename = title.strip().replace(' ', '').replace('“', '').replace('”', '').replace('|', '')
        filename = filename.replace('/', '-').replace('？', '').replace('\\', '').replace('：', ':')
        filename = filename.replace("<", "《").replace('>', '》').replace('*', '').replace('\n', '').replace("\"", "").replace('?', '')
        with open(filename + '.txt', 'w', encoding='utf8') as f:
            f.write(contents)

        bihu_item = BihuItemLoads(item=BihuspiderItem(), response=response)
        bihu_item.add_value('articleId', article_id)
        bihu_item.add_value('author', author)
        bihu_item.add_value('userId', user_id)
        bihu_item.add_value('title', title)
        bihu_item.add_value('articledesc', articledesc)
        bihu_item.add_value('money', money)
        bihu_item.add_value('ups', ups)
        bihu_item.add_value('comments', comments)
        bihu_item.add_value('create_time', create_time_stamp)
        bihu_item.add_value('update_time', update_time_stamp)
        bihu_item.add_value('content_url', full_content_url)
        bihu_item.add_value('content', contents)

        bihu_article_item = bihu_item.load_item()

        yield bihu_article_item

    # def parse_content(self, response):
    #     content = response.text
    #     bihu_item = BihuItemLoads(item=BihuspiderItem(), response=response)
    #     bihu_item.add_value('content', content)
    #     bihu_article_item = bihu_item.load_item()
    #
    #     yield bihu_article_item
