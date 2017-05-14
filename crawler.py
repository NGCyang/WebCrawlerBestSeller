import urllib2
import time
from bs4 import BeautifulSoup

class Spider:

    def __init__(self):
        self.url = 'https://www.adafruit.com/product/'

        #self.product_id = 3162
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        self.headers = {'User-Agent' : self.user_agent }

    def get_stock_num(self, product_id):
        url = self.url + str(product_id)
        request = urllib2.Request(url, headers = self.headers)
        try:
            response = urllib2.urlopen(request)
            page = response.read()
            print page
        except urllib2.URLError, e:
            print e



if __name__ == '__main__':
    spider = Spider()
    spider.get_stock_num(3162)
