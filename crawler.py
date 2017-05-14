import urllib2
import time
from bs4 import BeautifulSoup
import re
from pymongo import *

class Spider:
    def __init__(self):
        self.url = 'https://www.adafruit.com/product/'

        #self.product_id = 3162
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        self.headers = {'User-Agent' : self.user_agent }

    def get_page(self, product_id):
        url = self.url + str(product_id)
        request = urllib2.Request(url, headers = self.headers)
        try:
            response = urllib2.urlopen(request)
            page = response.read()
            return page
        except urllib2.URLError, e:
            print e
            return None

    def get_stock_num(self, product_id):
        page = self.get_page(product_id)
        if page is None:
            return None
        soup = BeautifulSoup(page, "lxml")
        item_info = {}
        #get product_id
        item_info['product_id'] = product_id

        # get product name
        item_info['product_name'] = soup.find('h1', attrs={'itemprop' : 'name'}).string

        # get all categorys
        breadcrumbs_div = soup.find('div', class_='breadcrumbs')
        categorys = []
        for a in breadcrumbs_div.find_all('a', href=re.compile("/category/")):
            categorys.append(a.attrs['href'].split('/')[2])
        item_info['categorys'] = categorys

        # get stock number
        storage_div = soup.find('div', class_='mobile-text-margins top-ten')
        storage_num = 0
        if storage_div.find('div', attrs = {'itemprop' : 'availability'}) is None:
            if storage_div.find('h2'):
                return None
            stock_text = storage_div.string.strip().lower().split()
            if stock_text[0] == 'in':
                storage_num = 100
            else:
                storage_num = int(stock_text[0])
        else:
            storage_num = 0;

        item_info['storage'] = storage_num
        return item_info

    def crawler_all_product(self, collection):
        for id in range(0, 3500):
            time.sleep(2s)
            data = self.get_stock_num(id)
            if data != None:
                collection.insert_one(data)



if __name__ == '__main__':
    spider = Spider()
    for id in range(3000, 3050):
        time.sleep(1)
        print spider.get_stock_num(id)
    #print spider.crawler_all_product()
