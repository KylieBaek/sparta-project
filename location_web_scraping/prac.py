from pymongo import MongoClient
import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup
from selenium import webdriver

if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('windows-size=1920x1080')
    options.add_argument('disable-gpu')
    gini = webdriver.Chrome('C:/Users/NTRION/Downloads/chromedriver_win32/chromedriver.exe', options=options)
    gini.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20190908')

    client = MongoClient('localhost', 27017)
    db = client.dbgini

    # 셀렉터
    # 순위 : #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
    # 이름 : #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
    # 가수 : #body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis

    soup = BeautifulSoup(gini.page_source, 'html.parser')
    songs = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
    # print(song)

for song in songs:
    person = song.select_one('td > a.artist.ellipsis').text.strip()
    name = song.select_one('td > a.title.ellipsis').text.strip()
    unwanted_rank = song.select_one('td.number > span')
    unwanted_rank.extract()
    rank = song.select_one('td.number').text.strip()
    # print(rank, name, person)
    db.songRanking.insert_one({'rank': rank, 'song': name, 'artist': person})


gini.quit()




from selenium import webdriver
from bs4 import BeautifulSoup

# setup Driver|Chrome : 크롬드라이버를 사용하는 driver 생성
driver = webdriver.Chrome('C:/Users/NTRION/Downloads/chromedriver_win32/chromedriver.exe')
driver.implicitly_wait(3)  # 암묵적으로 웹 자원을 (최대) 3초 기다리기
# Login
driver.get('https://nid.naver.com/nidlogin.login')  # 네이버 로그인 URL로 이동하기
driver.find_element_by_name('id').send_keys('naver_id')  # 값 입력
driver.find_element_by_name('pw').send_keys('mypassword1234')
driver.find_element_by_xpath(
    '//*[@id="frmNIDLogin"]/fieldset/input'
).click()  # 버튼클릭하기
driver.get('https://order.pay.naver.com/home')  # Naver 페이 들어가기
html = driver.page_source  # 페이지의 elements모두 가져오기
soup = BeautifulSoup(html, 'html.parser')  # BeautifulSoup사용하기
notices = soup.select('div.p_inr > div.p_info > a > span')

for n in notices:
    print(n.text.strip())