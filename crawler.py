import urllib2
import time
from bs4 import BeautifulSoup
import re
from pymongo import *

class Spider:
    def __init__(self):
        self.collection = None
        self.url = 'https://www.adafruit.com/'

        #self.product_id = 3162
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        self.headers = {'User-Agent' : self.user_agent }

    def get_page(self, product_id):
        url = self.url + 'product/' +str(product_id)
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

        # get all categories
        breadcrumbs_div = soup.find('div', class_='breadcrumbs')
        categories = []
        for a in breadcrumbs_div.find_all('a', href=re.compile("/category/")):
            categories.append(a.attrs['href'].split('/')[2])
        item_info['categories'] = categories

        # get stock number
        storage_div = soup.find('div', class_='mobile-text-margins top-ten')
        storage_num = 0
        if storage_div.find('div', attrs = {'itemprop' : 'availability'}) is None:
            # Discontinued
            if storage_div.find('h2'):
                return None
            stock_text = storage_div.string.strip().lower().split()

            if len(stock_text) == 0:
                # No Stock Information
                print "No Info"
                return None
            elif stock_text[0] == 'in':
                # In Stock
                storage_num = 100
            else:
                # Num In Stock
                storage_num = int(stock_text[0])
        else:
            # Out of Stock
            storage_num = 0

        item_info['storage'] = storage_num
        return item_info

    def crawler_all_product(self, collection):
        for id in range(0, 3500):
            print id
            time.sleep(1)
            data = self.get_stock_num(id)
            if data != None:
                collection.insert_one(data)

    def get_category_page(self, category_id):
        print category_id
        time.sleep(1)
        url = self.url + 'category/' +str(category_id)
        request = urllib2.Request(url, headers = self.headers)
        try:
            response = urllib2.urlopen(request)
            page = response.read()
            return page
        except urllib2.URLError, e:
            print e
            return None

    def get_from_category_entry(self,):
        url = self.url + "categories"
        request = urllib2.Request(url, headers = self.headers)
        try:
            response = urllib2.urlopen(request)
            page = response.read()
            soup = BeautifulSoup(page, "lxml")
            for h3 in soup.find_all('h3'):
                a = h3.find('a', href=re.compile("^category/"))
                if a is None:
                    continue
                else:
                    category_id = int(a.attrs['href'].split('/')[1])
                    self.get_stock_num_from_categories(category_id)
        except urllib2.URLError, e:
            print e
            return


    def get_stock_num_from_categories(self,category_id):
        page = self.get_category_page(category_id)
        soup = BeautifulSoup(page, "lxml")
        product_list = soup.find('div', id='productListing')
        for row in product_list.find_all('div', class_='row product-listing'):
            item_info = {}
            item_info['categories'] = [category_id]
            product_a = row.find('a', href=re.compile("^/product/"))
            item_info['product_name'] = product_a.attrs['data-name']
            item_info['product_id'] = product_a.attrs['data-pid']
            # id_div = row.find('div', class_='product_id')
            # item_info['product_id'] = int(id_div.find('span').string)
            price_span = row.find('span', attrs={'itemprop' : 'price'})
            if price_span != None:
                item_info['price'] = float(price_span.string.replace(',', ''))
            else:
                item_info['price'] = None

            stock_span = row.find('span', attrs={'itemprop' : 'availability'})
            if stock_span == None:
                #stock_string = None
                continue
            elif stock_span.string.strip().lower() == 'discontinued':
                continue
            elif stock_span.string.strip().lower() == 'coming soon':
                continue
            else:
                stock_string = stock_span.string

            item_info['storage'] = self.get_num_from_string(stock_string)
            self.update_in_database(item_info)
            # print item_info


    def update_in_database(self, item_info):
        original_info = self.collection.find_one({"product_id" : item_info['product_id']})
        if original_info == None:
            self.collection.insert_one(item_info)
        else:
            # for category_id in original_info['categories']:
            #     item_info['categories'].append(category_id)
            categories_set = set()
            for category in item_info['categories']:
                categories_set.add(category)
            for category in original_info['categories']:
                categories_set.add(int(category))
            self.collection.update_one(
                    { 'product_id' : item_info['product_id']},
                    {"$set": {
                            "categories":list(categories_set),
                            "storage":item_info['storage'],
                            "price":item_info['price']
                    }})

    def set_datebase(self, collection):
        self.collection = collection

    def get_num_from_string(self, string):
        stock_text = string.strip().lower().split()
        if stock_text[0] == 'in':
            # In Stock
            return 100
        elif stock_text[0] == 'out':
            # Out of Stock
            return 0
        else:
            # Num in stock
            return int(stock_text[0])


if __name__ == '__main__':
    client = MongoClient('localhost', 27017)
    db = client.crawler
    collection = db.storage_test

    print collection.count()
    # spider = Spider()
    # spider.set_datebase(collection)
    # #spider.get_category_entry()
    # spider.get_stock_num_from_categories(851)
    # for item in collection.find().limit(20):
    #     print item


    # for id in range(3000, 3050):
    #     time.sleep(1)
    #     print spider.get_stock_num(id)
    #print spider.crawler_all_product()
