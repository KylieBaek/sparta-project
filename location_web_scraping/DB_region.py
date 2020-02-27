from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject

loc = list(db.location.find({'region':'chungbuk'}))
totalvisit =0
for n in loc:
    totalvisit = totalvisit +n['visitcount']

print(totalvisit)
doc = {'region': 'chungbuk',
       'region_ko':'충청북도',
       'visitcount': totalvisit,
       'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcS7QoQqHs3LbQWplKaH2fLRrSfHS1rnkaDNJpAOu3mNjzDXkvrO'
       }
print(doc)
db.region.insert_one(doc)
