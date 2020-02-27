from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject
driver = webdriver.Chrome('C:/Users/NTRION/Downloads/chromedriver_win32/chromedriver.exe')

spots = list(db.gyeongbuk.find({}))

for spot in (spots):
    loc = spot['location']
    if loc.find('연중') != -1:
        edits =  db.gyeongbuklink.find_one({'name': spot['name']})
        print(edits)
        driver.get(edits['link'])

        new_loc =driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div[2]/div/div/ul/li[2]/span').text
        db.gyeongbuk.update_one({'location': loc}, {'$set': {'location': new_loc}})


driver.quit()

