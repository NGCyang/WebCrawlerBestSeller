# -*- coding: utf-8 -*-

from pymongo import *
from flask import Flask, json, request
from crawler import Spider
from bson import json_util

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.crawler
collection = db.storage

'''
Intital
'''
@app.before_first_request
def start_crawler():
    collection.remove()
    spider = Spider()
    spider.crawler_all_product(collection)
    #collection.insert_many(spider.crawler_all_product())


#def daily_crawler(spider):


'''
Routing
'''
@app.route('/')
def main():
    return json.dumps({"total_product_number" : collection.count()})

@app.route('/bestseller', methods=['GET'])
def get_bestseller():
    cursor = collection.find().sort("storage",ASCENDING).limit(20)
    #json_docs = [json.dumps(doc, default=json_util.default) for doc in cursor]
    return json_util.dumps(cursor)

@app.route('/bestseller/category/<id>', methods=['GET'])
def get_category_bestseller(id = None):
    cursor = collection.find({ "categorys" : id }).sort("storage",ASCENDING).limit(20)
    return json_util.dumps(cursor)

@app.route('/bestseller/v2', methods=['GET'])
def get_bestseller_v2():
    cursor = collection.find("datetime" < )

if __name__ == "__main__":
    app.run(host='0.0.0.0')
