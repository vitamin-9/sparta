from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request
from operator import itemgetter
import math
import csv
from bs4 import BeautifulSoup

app = Flask(__name__)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.wcinfo

@app.route('/')
def home():
    return render_template('index.html')

# API 역할을 하는 부분
@app.route('/finding', methods=['post'])
def matching():
    lat_rcv = float(request.form['lat_give'])
    long_rcv= float(request.form['long_give'])

    print (lat_rcv, long_rcv)

    wc_data = list(db.seoul_wc.find({}, {'_id':False}))
    wcdata = [{'name' : 'criteria', 'lat': lat_rcv, 'long': long_rcv, 'dist': 0}]
    for wc_info in wc_data:
        lat_ref = float(wc_info['lat'])
        long_ref = float(wc_info['long'])
        dist = math.sqrt(math.pow(lat_rcv - lat_ref, 2) + math.pow(long_rcv - long_ref, 2))
        tmp_wcdata={
            'name' : wc_info['name'],
            'lat' : lat_ref,
            'long' : long_ref,
            'dist' : dist
        }
        wcdata.append(tmp_wcdata)

    wclist=sorted(wcdata, key=itemgetter('dist'))
    wcresult = [
        wclist[0], wclist[1], wclist[2], wclist[3], wclist[4], wclist[5]
    ]
    # print (wcresult)
    db.userrecord.remove({})
    db.userrecord.insert_many(wcresult)
    return jsonify({'result': 'success', 'msg': 'matching success'})

@app.route('/show', methods=['GET'])
def showing():
    closewc = list(db.userrecord.find({}, {'_id': 0}))
    return jsonify({'result': 'success', 'fivewc': closewc})



    # for wc_info in wc_data:
    #     print(wc_info)
    #     lat_ref : wc_info{'lat'}
        # long_ref : wc_ifo{'long'}
        # dist = math.sqrt(math.pow(lat_rcv - lat_ref, 2) + math.pow(long_rcv - long_ref, 2))
        # wc_tmp = {
        #     'name' : wc_info[1],
        #     'lat' : wc_info{'lat'},
        # }
        #         db.seoul_wc.insert_one(wc)
        #
        # if wc_ifo{'lat'}

    # 1. 클라이언트로부터 데이터를 받기
#
#
#
# @app.route('/memo', methods=['GET'])
# def m():
#
#     # 1. 모든 document 찾기 & _id 값은 출력에서 제외하기
#     result = list(db.articles.find({}, {'_id':False}))
#
#     # 2. articles라는 키 값으로 영화정보 내려주기
#     return jsonify({'result':'success', 'articles': result})

#
# # 서울시 공공화장실 (CSV) 정보 불러오기
# with open('./data/seoul_public_toilet.csv', 'r') as tmp:
#     data = csv.reader(tmp)
#     next(data)
#     for wc_info in data:
#         wc ={
#             'name' : wc_info[1],
#             'lat' : wc_info[7],
#             'long' : wc_info[6]
#         }
#         db.seoul_wc.insert_one(wc)
# #



#
# 	# 3. mongoDB에 데이터 넣기
#
#     article = {
#         'url': url_receive,
#         'comment' : comment_receive,
#         'image' : og_image,
#         'title' : og_title,
#         'desc' : og_description
#     }
#     db.articles.insert_one(article)
#
#
#     return jsonify({'result': 'success', 'msg':'POST 연결되었습니다!'})
#
if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)