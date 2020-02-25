from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject
driver = webdriver.Chrome('C:/Users/NTRION/Downloads/chromedriver_win32/chromedriver.exe')

spots = list(db.gyeongbuklink.find({}))

for spot in spots:
    driver.get(spot['link'])
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    image =soup.select_one('meta[property="og:image"]')['content']
    location =driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div[2]/div/div/ul/li[3]/span').text
    description=driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[3]/div[1]/div/div/p').text
    if location is not None:
        doc = {'name': spot['name'],
               'image':image ,
               'location': location,
               'description':description}
        db.gyeongbuk.insert_one(doc)

driver.quit()