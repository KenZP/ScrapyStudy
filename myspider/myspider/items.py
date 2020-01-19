# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import datetime

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def date_convert(value):
    try:
        s_timestamp = int(value / 1000)
        date_array = datetime.datetime.utcfromtimestamp(s_timestamp)
        create_date = date_array.strftime("%Y-%m-%d %H:%M:%S")
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


class BihuItemLoads(ItemLoader):
    default_output_processor = TakeFirst()


class BihuspiderItem(scrapy.Item):
    # define the fields for your item here like:
    userId = scrapy.Field()
    articleId = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    articledesc = scrapy.Field()
    content_url = scrapy.Field()
    content = scrapy.Field()
    money = scrapy.Field()
    ups = scrapy.Field()
    comments = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    update_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )

    def get_insert_sql(self):
        # 插入币乎article表的sql语句
        insert_sql = """
            insert into bihuarticle(userId, articleId, author, title, articledesc, content_url, money,
              ups, comments, create_time, update_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content_url=VALUES(content_url), comments=VALUES(comments), money=VALUES(money),
              update_time=VALUES(update_time), ups=VALUES(ups)
        """

        # create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        # update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["userId"], self["articleId"], self["author"],
            self["title"], self["articledesc"], self["content_url"],
            self["money"], self["ups"], self["comments"],
            self["create_time"], self["update_time"],
        )

        return insert_sql, params


class StockspiderItem(scrapy.Item):
    # define the fields for your item here like:
    deal_date = scrapy.Field()
    code = scrapy.Field()
    name = scrapy.Field()
    begin = scrapy.Field()
    end = scrapy.Field()
    max = scrapy.Field()
    min = scrapy.Field()
    volume = scrapy.Field()
    amount = scrapy.Field()
    PE = scrapy.Field()
    PB = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )
    update_time = scrapy.Field(
        input_processor=MapCompose(date_convert),
    )

    def get_insert_sql(self):
        # 插入币乎article表的sql语句
        insert_sql = """
            insert into stock_info(deal_date, code, name, begin, end, articledesc, content_url, money,
              ups, comments, create_time
              ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
              ON DUPLICATE KEY UPDATE content_url=VALUES(content_url), comments=VALUES(comments), money=VALUES(money),
              update_time=VALUES(update_time), ups=VALUES(ups)
        """

        # create_time = datetime.datetime.fromtimestamp(self["create_time"]).strftime(SQL_DATETIME_FORMAT)
        # update_time = datetime.datetime.fromtimestamp(self["update_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["userId"], self["articleId"], self["author"],
            self["title"], self["articledesc"], self["content_url"],
            self["money"], self["ups"], self["comments"],
            self["create_time"], self["update_time"],
        )

        return insert_sql, params
