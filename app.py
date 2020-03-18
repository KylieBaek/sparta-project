from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

import requests
from bs4 import BeautifulSoup
from operator import itemgetter
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


# @app.route('/regionpage')
# def regionpage():
#      return render_template('region.html')


## 1. main page 지역 listing API
@app.route('/main', methods=['GET'])
def listing():
    regions = list(db.region.find({}, {'_id': 0}))
    sort_region = sorted(regions, key=itemgetter('visitcount', 'region_ko'))  # visitcount기준으로 오름차순정렬
    sort_region.reverse()
    for s in sort_region:
        print(s)
    return jsonify({'result': 'success', 'regions': sort_region})


# 2. 지역별 상세 page로 이동 API

@app.route('/region', methods=['GET'])
def regiondetail():
    region_receive = request.args.get('region_give')

    # locations = list(db.location.find({'region': region_receive}, {'_id': 0}))
    # sort_location = sorted(locations, key=itemgetter('visitcount', 'name'))  # visitcount기준으로 오름차순정렬
    # sort_location.reverse()
    #
    # for s in sort_location:
    #     print(s)

    # locations_data = json.dumps(sort_location, ensure_ascii=False)

    data = {'region': region_receive}
    return render_template('region.html', data=data)



@app.route('/region-locations', methods=['GET'])
def regiondetail_locations():
    region_receive = request.args.get('region_give')

    locations = list(db.location.find({'region': region_receive}, {'_id': 0}))
    sort_location = sorted(locations, key=itemgetter('visitcount', 'name'))  # visitcount기준으로 오름차순정렬
    sort_location.reverse()

    for s in sort_location:
        print(s)

    return jsonify({'result': 'success', 'region': region_receive, 'locations':sort_location})


@app.route('/visitup', methods=['POST'])
def saving():
    url_receive = request.form['url_give']  # 클라이언트로부터 url을 받는 부분
    comment_receive = request.form['comment_give']  # 클라이언트로부터 comment를 받는 부분

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    og_image = soup.select_one('meta[property="og:image"]')
    og_title = soup.select_one('meta[property="og:title"]')
    og_description = soup.select_one('meta[property="og:description"]')

    url_image = og_image['content']
    url_title = og_title['content']
    url_description = og_description['content']

    article = {'url': url_receive, 'comment': comment_receive, 'image': url_image,
               'title': url_title, 'desc': url_description}

    db.articles.insert_one(article)

    return jsonify({'result': 'success'})



if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
