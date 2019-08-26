from pymongo import MongoClient
from MySQLdb import *
from random import randrange
from datetime import timedelta, datetime

#MySQL 로그인 정보
###################################
DB_IP = 'localhost'
DB_ID = "root"
DB_PW = "imlisgod"
###################################

#MySQL 접속
MySQL_db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='namuwiki', charset='utf8mb4', cursorclass=cursors.DictCursor)

###############################################################
###############################################################

#mongoDB 클래스 객체 할당
mongoDB_client = MongoClient()
#mongoDB 접속
mongoDB_client = MongoClient('localhost', 27017)
#mongoDB db객체 할당받기
mongoDB_db = mongoDB_client["namuwiki"]
#mongoDB collection객체 할당받기
mongoDB_collection = mongoDB_db["post"]

###############################################################
###############################################################
#Insert rand_num on MongoDB
'''
f = open('rand_num.txt', 'r')
for post in mongoDB_collection.find():
	f_rand_num = f.readline()
	f_rand_num = int(f_rand_num)

	mongoDB_collection.update({'_id': post['_id']}, {'$set': {'rand_num': f_rand_num}})
	print(f_rand_num)
'''
#d = datetime.datetime.strptime("2017-10-13T10:53:53.000Z", "%Y-%m-%dT%H:%M:%S.000Z")

#Create rand_date Function
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

d1 = datetime.strptime('2000-01-01T00:00:00Z', '%Y-%m-%dT%H:%M:%SZ')
d2 = datetime.strptime('2020-12-31T23:59:59Z', '%Y-%m-%dT%H:%M:%SZ')

for post in mongoDB_collection.find():
	temp = random_date(d1, d2)
	mongoDB_collection.update({'_id': post['_id']}, {'$set': {'date': temp }})
	print(temp)

