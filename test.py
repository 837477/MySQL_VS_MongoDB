import time
import sys
from pymongo import MongoClient
from MySQLdb import *

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

#int TEST
##############################################################
'''
f = open('random.txt', 'r')
random = []

for i in range(1000):
	random.append(int(f.readline()))
'''
##############################################################

#string TEST
##############################################################

topic = {'안녕', '입니다', '컴퓨터', '아이템', '섹스', '이다', '한다', '금지', '뷁뀹뽕', '뭵뷁읭', '그래서', '근디', '정부', '대기', '왼쪽', '오른쪽', '아래', '배틀그라운드', '게임', '휴대폰', '스마트폰', '데이터', '오스트렐랄로피테쿠스', '호모사피엔스', '이누야샤', '허걱', '회사', '퓨즈', '고압선', '스티븐잡스', '미국', '대한민국', '일본', '중국', 'hello', 'hi', 'world', 'is', 'are', 'He', 'She', 'We', 'They', 'It', 'That', 'and', 'or', 'not', 'WIFI', 'LTE'}

topic_str = "#redirect 느낌표" #실제 데이터에 있는 내용임.

#FULLTEXT INDEX ngram_idx(title) WITH PARSER ngram
#alter table post add FULLTEXT INDEX ngram_idx(_text) WITH PARSER ngram
#ALTER TABLE tablename DROP INDEX indexname;

##############################################################
'''
#ARRAY
##############################################################
topic ={'안녕', '허걱', '이누야샤', '근디', '이다', '한다', '금지', '대한민국', '미국', '뷁뭵웱', 'Hello', 'Hi', 'WIFI', 'LTE', 'They', 'wonderful', 'sejong', 'phone', 'computer', 'aksfnldskfnalks'}
contributors_list = [['samduk', 'R:ddy1456'], ['e080hsm', '49.163.93.241'], ['UnofficialNamuImgServer', '222.112.45.157'], ['guylian', 'FluffyBunny'], ['alfalfa', 'asia'], ['yul', 'R:franch122'], ['R:camellia0726', 'ssangmun2'], ['gkscnsrb', 'mildbot'], ['actanonverba', 'sky_nintendo'], ['Cocapepper', '220.94.30.201'], ['sideout', 'reviseandadd'], ['Great_Red', 'shj895'], ['zcxe2001', 'R:ironnokana'], ['122.40.9.176', 'R:Souther']]
##############################################################
'''
'''
#MySQL int TEST
start = time.time()

with MySQL_db.cursor() as cursor:
	sql = "SELECT title FROM post WHERE rand_num = %s;"

	for num in random:
		cursor.execute(sql, (num,))
		result = cursor.fetchall()
		print(result)

print("소요시간 :", time.time() - start)
'''
'''
#MongoDB int TEST
start = time.time()

for num in random:
	result = list(mongoDB_collection.find({'rand_num': num}, {'_id':0, 'title':1}))
	print(result)

print("소요시간 :", time.time() - start)
'''
#STRING(Equal)
##############################################################
##############################################################
'''
#MySQL string(Equal) TEST
start = time.time()

with MySQL_db.cursor() as cursor:
	sql = "SELECT title FROM post WHERE _text = %s;"

	print("MySQL string(Equal) TEST")
	cursor.execute(sql, (topic_str,))
	result = cursor.fetchall()

print("소요시간 :", time.time() - start)
'''
'''
#MongoDB string(Equal) TEST
start = time.time()

print("MongoDB string(Equal) TEST")
result = list(mongoDB_collection.find({'text': topic_str}, {'_id':0, 'title':1}))

print("소요시간 :", time.time() - start)
'''
#STRING(LIKE)
##############################################################
##############################################################
'''
#MySQL string(NOINDEX) TEST
start = time.time()

with MySQL_db.cursor() as cursor:
	sql = "SELECT count(*) AS cnt FROM post WHERE _text LIKE %s"

	print("MySQL string(NOINDEX) TEST")
	for topic_one in topic:
		temp_topic = '%' + topic_one + '%'
		cursor.execute(sql, (temp_topic,))
		result = cursor.fetchone()
		print(topic_one,'의 갯수: ', result['cnt'])

print("소요시간 :", time.time() - start)
'''
'''
#MySQL string(FULLTEXT INDEX) TEST
start = time.time()

with MySQL_db.cursor() as cursor:
	sql = "SELECT COUNT(*) AS cnt FROM post WHERE MATCH (_text) AGAINST(%s IN BOOLEAN MODE);"

	print("MySQL string(FULLTEXT INDEX) TEST")
	for topic_one in topic:
		cursor.execute(sql, (topic_one,))
		result = cursor.fetchone()
		print(topic_one,'의 갯수: ', result['cnt'])

print("소요시간 :", time.time() - start)
'''
'''
#MongoDB string(NOINDEX) TEST
start = time.time()

print("MongoDB string(NOINDEX INDEX) TEST")
for topic_one in topic:
	result = mongoDB_collection.find({'text': {'$regex': topic_one}}).count()
	print(topic_one,'의 갯수: ', result)

print("소요시간 :", time.time() - start)
'''
'''
#MongoDB string(FULLTEXT INDEX) TEST
start = time.time()

print("MongoDB string(FULLTEXT INDEX) TEST")
for topic_one in topic:
	result = mongoDB_collection.find({'$text': {'$search': topic_one}}).count()
	print(topic_one,'의 갯수: ', result)

print("소요시간 :", time.time() - start)
'''
#ARRAY
##############################################################
##############################################################
'''
#MySQL ARRAY(JOIN)_20개 contributors TEST
count = 0
start = time.time()

with MySQL_db.cursor() as cursor:
	sql = "SELECT A.pt_id from (SELECT * FROM post WHERE _text LIKE %s) A LEFT JOIN (SELECT pt_id FROM post_contributors WHERE content = %s OR content = %s) B ON A.pt_id = B.pt_id"

	print("MySQL ARRAY(JOIN) TEST")
	for topic_one in topic:
		count += 1
		temp_topic = '%' + topic_one + '%'
		for contributors in contributors_list:
			cursor.execute(sql, (temp_topic, contributors[0], contributors[1],))
			result = cursor.fetchone()
		print(count)

print("소요시간 :", time.time() - start)
'''
'''
#MongoDB ARRAY_20개 contributors TEST
count = 0
start = time.time()

print("MongoDB ARRAY TEST")
for topic_one in topic:
		count += 1
		for contributors in contributors_list:
			result = mongoDB_collection.find({'$and': [ {'text': {'$regex': topic_one}}, {'$or': [ {'contributors': contributors[0] }, {'contributors': contributors[1]} ]} ]}).count()
		print(count)

print("소요시간 :", time.time() - start)
'''
'''
#MySQL ARRAY(JOIN)_namubot TEST
start = time.time()

with MySQL_db.cursor() as cursor:
	sql = "SELECT COUNT(A.pt_id) AS cnt FROM (SELECT * FROM post WHERE _text LIKE %s) A LEFT JOIN (SELECT pt_id FROM post_contributors WHERE content = %s) B ON A.pt_id = B.pt_id"

	print("MySQL ARRAY(JOIN)_NAMUBOT(COUNT) TEST")
	for topic_one in topic:
		temp_topic = '%' + topic_one + '%'
		cursor.execute(sql, (temp_topic, 'namubot'))
		result = cursor.fetchone()
		print('namubot이 작성한', topic_one, '단어가 포함된 글 갯수', result['cnt'])

print("소요시간 :", time.time() - start)
'''
'''
#MongoDB ARRAY_namubot TEST
start = time.time()

print("MongoDB ARRAY_NAMUBOT(COUNT) TEST")

#for topic_one in topic:
result = mongoDB_collection.find({'$and': [ {'text': {'$regex': '이누야샤'}}, {'$or': [ {'contributors': 'namubot' } ]} ]}).count()
print('namubot이 작성한', '이누야샤', '단어가 포함된 글 갯수', result)

print("소요시간 :", time.time() - start)
'''