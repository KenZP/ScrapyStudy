import requests
from lxml import etree
import tushare as ts
from sqlalchemy import create_engine
from myspider.settings import tushare_key


class StockCodeSpider:
    def __init__(self):
        self.url = ['https://hq.gucheng.com/gpdmylb.html', 'https://hq.gucheng.com/cybgp.html']
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0',
        }

    def get_stock_code(self):
        stock_code_list = []
        for url in self.url:
            resp = requests.get(url, headers=self.headers)
            root = etree.HTML(resp.content)
            stock_codes = root.xpath("//*[@class='stockTable']//a/text()")
            for code in stock_codes:
                stock_code = code.split('(')[1].split(')')[0]
                stock_code_list.append(stock_code)
        return stock_code_list


class GetStockCodes:
    def save_to_mysql(self, df):
        # 存入mysql数据库
        engine = create_engine('mysql://root:root@127.0.0.1/stockcode?charset=utf8')
        # 更新数据到现有表
        df.to_sql('stock_lists', engine, if_exists='replace')

    def get_stock_list(self):
        ts.set_token(tushare_key)
        pro = ts.pro_api()
        # stock_list = pro.stock_basic(exchange='', list_status='L', fields='symbol, name, industry, list_date, is_hs')
        stock_code_list = pro.stock_basic(exchange='', list_status='L', fields='')
        self.save_to_mysql(stock_code_list)
        stock_code_list.to_csv('stock_lists.csv')

        # code = stock_list.iloc[0, 1]
        code_list = stock_code_list['symbol'].values
        # stock_list.to_csv('stock_lists.csv')
        # print(code_list)
        return code_list


if __name__ == '__main__':
    # 爬虫获取股票代码列表
    stock_spider = StockCodeSpider()
    stock_codes = stock_spider.get_stock_code()
    final_stock_codes = list(set(stock_codes))
    for code in final_stock_codes:
        print(code)

    # 通过调用tushare借口获取股票代码列表
    get_stock_code = GetStockCodes()
    stock_list = get_stock_code.get_stock_list()
    for code in stock_list:
        print(code)


