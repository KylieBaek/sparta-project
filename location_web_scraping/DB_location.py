from pymongo import MongoClient
import random
#지역별DB를 하나의 DB로 합치기
client = MongoClient('localhost', 27017)
db = client.dbproject

locations = list(db.ulsan.find({}))
for n in locations:
    doc = { 'region': 'ulsan',
             'name': n['name'],
            'location': n['location'],
            'image':n['image'],
            'description' : n['description'],
            'visitcount': random.randint(1, 1000)
            }
    print(doc)
    db.location.insert_one(doc)