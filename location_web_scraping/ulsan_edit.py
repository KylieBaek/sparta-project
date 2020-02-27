from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject
# driver = webdriver.Chrome('C:/Users/NTRION/Downloads/chromedriver_win32/chromedriver.exe')

spots = list(db.ulsan.find({}))

for spot in (spots):
    loc = spot['location']
    if loc.find('강원') != -1:

        doc ={
            'name':spot['name'],
            'image':spot['image'],
            'location':spot['location'],
            'description':spot['description']
        }

        db.ulsan.delete_one({'location': loc})
        db.kangwon.insert_one(doc)


# driver.quit()

