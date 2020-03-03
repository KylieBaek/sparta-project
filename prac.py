from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject

doc = {'regioncount': 50}
print(doc)

db.region.update({},
                 {$set: {"new_field": 1}},
{upsert: false,
 multi: true})
