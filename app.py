# -*- coding: utf-8 -*-

from pymongo import *
from flask import Flask, json, request
from crawler import Spider
from bson import json_util
import sys
from datetime import datetime
from threading import Timer


app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.crawler
#collection = db.storage
collection = db.storage_test

spider = Spider()
spider.set_datebase(collection)

'''
Intital
'''
@app.before_first_request
def start_crawler():
    spider.get_from_category_entry()
    #daily_crawler()

def daily_crawler():
    spider.get_from_category_entry()
    x = datetime.today()
    y = x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
    delta_t = y-x
    secs = delta_t.seconds+1
    t = Timer(secs, daily_crawler)
    t.start()


'''
Routing
'''
@app.route('/')
def main():
    return json.dumps({"total_product_number" : collection.count()})


@app.route('/bestseller', methods=['GET'])
@app.route('/bestseller/page<int:page>', methods=['GET'])
def get_bestseller(page=1):
    _num_per_page = 20
    _lower_price = 0.0
    _upper_price = sys.float_info.max
    if 'lower_price' in request.args and 'upper_price' in request.args:
        _lower_price = float(request.args.get('lower_price',''))
        _upper_price = float(request.args.get('upper_price',''))

    cursor = collection.find({'price' : { '$gte' :  _lower_price, '$lt' : _upper_price}}).sort("storage",ASCENDING).skip((page-1)*_num_per_page).limit(_num_per_page)
    #json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
    return json_util.dumps(cursor)

@app.route('/category/<int:category_id>/bestseller', methods=['GET'])
@app.route('/category/<int:category_id>/bestseller/page<int:page>', methods=['GET'])
def get_category_bestseller(category_id = None, page=1):
    _num_per_page = 20
    _lower_price = 0.0
    _upper_price = sys.float_info.max
    if 'lower_price' in request.args and 'upper_price' in request.args:
        _lower_price = float(request.args.get('lower_price',''))
        _upper_price = float(request.args.get('upper_price',''))

    cursor = collection.find({ "categories" : category_id, 'price' : { '$gte' :  _lower_price, '$lt' : _upper_price} }).sort("storage",ASCENDING).skip((page-1)*_num_per_page).limit(_num_per_page)
    return json_util.dumps(cursor)

# @app.route('/bestseller/v2', methods=['GET'])
# def get_bestseller_v2():
#     cursor = collection.find("datetime" < )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
