from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta                      # 'dbsparta'라는 이름의 db를 만듭니다.

## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('hw7-4_index.html')

## API 역할을 하는 부분
@app.route('/orders', methods=['POST'])
def write_orders():
    name_receive = request.form['name_give']
    qtt_receive = request.form['qtt_give']
    addr_receive = request.form['addr_give']
    phone_receive = request.form['phone_give']
    order ={
        'name' : name_receive,
        'qtt': qtt_receive,
        'addr': addr_receive,
        'phone': phone_receive,
    }

    db.orders.insert_one(order)
    return jsonify({'result':'success', 'msg': '주문이 성공적으로 완료됐습니다.'})

@app.route('/orders', methods=['GET'])
def read_orders():
    orders = list(db.orders.find({}, {'_id':0}))
    return jsonify({'result':'success', 'orders': orders})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)