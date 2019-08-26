from flask import Flask, render_template, jsonify
from flask_cors import CORS

from pymongo import MongoClient
from operator import itemgetter
import time

#mongoDB 클래스 객체 할당
mongoDB_client = MongoClient()
#mongoDB 접속
mongoDB_client = MongoClient('localhost', 27017)
#mongoDB db객체 할당받기
mongoDB_db = mongoDB_client["namuwiki"]
#mongoDB collection객체 할당받기
mongoDB_collection = mongoDB_db["post"]

'''
#SORT WITH PYTHON
##############################################################
##############################################################
DataSet = list(mongoDB_collection.find({}, {'_id':0, 'title':1, 'rand_num':1, 'date':1}))

#INT sort
start = time.time()
sort_result = sorted(DataSet, key=itemgetter('rand_num'))
print("INT sort 소요시간 :", time.time() - start)

#STRING sort
start = time.time()
sort_result = sorted(DataSet, key=itemgetter('title'))
print("STRING sort 소요시간 :", time.time() - start)

#DATE sort
start = time.time()
sort_result = sorted(DataSet, key=itemgetter('date'))
print("DATE sort 소요시간 :", time.time() - start)
'''

#SORT WITH JAVASCRIPT
##############################################################
##############################################################
application = Flask(__name__, instance_relative_config=True)
cors = CORS(application)

DataSet = list(mongoDB_collection.find({}, {'_id':0, 'title':1, 'rand_num':1, 'date':1}))

@application.route('/')
def root():
	return jsonify(
		result = "success")

@application.route('/test')
def test():
	return jsonify(
		result = "success",
		DataSet = DataSet)

if __name__ == '__main__':
	application.run(host='0.0.0.0', port=5000, debug=True)

