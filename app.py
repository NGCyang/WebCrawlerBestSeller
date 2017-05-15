# -*- coding: utf-8 -*-

from pymongo import *
from flask import Flask, json, request
from crawler import Spider
from bson import json_util
import sys

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.crawler
#collection = db.storage
collection = db.storage_test

'''
Intital
'''
# @app.before_first_request
# def start_crawler():
#     collection.remove()
#     spider = Spider()
#     spider.crawler_all_product(collection)

#def daily_crawler(spider):

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
