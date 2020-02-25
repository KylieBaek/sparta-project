import time
from selenium import webdriver
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbproject

driver = webdriver.Chrome('C:/Users/NTRION/Downloads/chromedriver_win32/chromedriver.exe')
driver.get('https://korean.visitkorea.or.kr/search/search_list.do?keyword=%EC%A0%9C%EC%A3%BC%EB%8F%84&temp=')
driver.implicitly_wait(3)  # 암묵적으로 웹 자원을 (최대) 3초 기다리기

driver.find_element_by_xpath('//*[@id="tabView4"]/a').click()  # 여행지 클릭
driver.find_element_by_xpath('//*[@id="3"]').click()  # 인기순 클릭
time.sleep(3)

soup = BeautifulSoup(driver.page_source, 'html.parser')  # BeautifulSoup사용하기

idx = 2

for i in range(5):
    li_index = 1
    spots = soup.select('#contents > div > div.box_leftType1 > ul > li >div.area_txt ')
    for spot in spots:
        # name = spot.select_one('div > a').text()
        name_key = '//*[@id="contents"]/div/div[1]/ul/li[{index}]/div[2]/div/a'.format(index=li_index)
        name = driver.find_element_by_xpath(name_key).text

        id = spot.select_one('div > a')
        detail_id = id.attrs['onclick'].split(',')[1].split('"')[1]
        detail_link = 'https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid={detail_id}'.format(
            detail_id=detail_id)

        print(name, detail_link)
        if detail_link is not None:
            doc = {'name': name, 'link': detail_link}
            db.jejulink.insert_one(doc)

        li_index = li_index + 1

    path = '/html/body/div[2]/div/div[1]/div[3]/a[{idx}]'.format(idx=idx)  # 다음페이지로 이동
    driver.find_element_by_xpath(path).click()
    idx = idx + 1
    time.sleep(5)

driver.quit()
