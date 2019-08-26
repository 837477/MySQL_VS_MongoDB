from pymongo import MongoClient
from MySQLdb import *

#MySQL 로그인 정보
###################################
DB_IP = 'localhost'
DB_ID = "root"
DB_PW = "imlisgod"
###################################

#MySQL 접속
MySQL_db = connect(host=DB_IP , user=DB_ID, password=DB_PW, charset='utf8mb4', cursorclass=cursors.DictCursor)

#MySQL DB 생성
with MySQL_db.cursor() as cursor:
	sql = "CREATE DATABASE IF NOT EXISTS namuwiki"
	cursor.execute(sql)
MySQL_db.commit()
MySQL_db.close()

MySQL_db = connect(host=DB_IP, user=DB_ID, password=DB_PW, db='namuwiki', charset='utf8mb4', cursorclass=cursors.DictCursor)

#MySQL TABLE 생성
with MySQL_db.cursor() as cursor:
	sql = open("table_post.sql").read()
	cursor.execute(sql)
	sql = open("table_post_contributors.sql").read()
	cursor.execute(sql)
MySQL_db.commit()

###################################
#mongoDB 클래스 객체 할당
mongoDB_client = MongoClient()
#mongoDB 접속
mongoDB_client = MongoClient('localhost', 27017)
#mongoDB db객체 할당받기
mongoDB_db = mongoDB_client["namuwiki"]
#mongoDB collection객체 할당받기
mongoDB_collection = mongoDB_db["post"]
###################################


for post in mongoDB_collection.find():
	with MySQL_db.cursor() as cursor:
		#post 삽입
		sql = "INSERT INTO post(_id, namespace, title, _text, rand_num) VALUES(%s, %s, %s, %s, %s);"
		cursor.execute(sql, (post['_id'], post['namespace'], post['title'], post['text'], post['rand_num'],))

		sql = "SELECT MAX(pt_id) AS pt_id FROM post;"
		cursor.execute(sql)
		pt_id = cursor.fetchone()
		pt_id = pt_id['pt_id']

		#contributors 리스트 테이블 삽입
		for contributor in post['contributors']:
			sql = "INSERT INTO post_contributors(pt_id, content) VALUES(%s, %s);"
			cursor.execute(sql, (pt_id, contributor,))
	MySQL_db.commit()
MySQL_db.close()



