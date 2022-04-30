from cgitb import text
from email import header
from msilib.schema import TextStyle
from urllib.request import Request, urlopen
import requests, re
import pandas as pd
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

def getsoup(url): #BeautifulSoup를 사용해 HTML Request
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Whale/3.12.129.46 Safari/537.36'}
    res = requests.get(url, headers=headers)
    return BeautifulSoup(res.content, 'html.parser')

def getDateRange():
    START_DATE = datetime.today() #오늘 날짜(시작날짜)
    END_DATE = datetime.strptime("20220601", "%Y%m%d")
    
    DATE_RANGE = []
    while START_DATE.strftime("%Y%m%d") != END_DATE.strftime("%Y%m%d"):
        DATE_RANGE.append(START_DATE.strftime("%Y%m%d"))
        START_DATE += timedelta(days=1)
    
    return DATE_RANGE

def getMainCategoryUrl():
    URL_LIST = []

    BASE_URL = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1='
    MAIN_CATEGORY = ['100', '101', '102', '103', '104', '105']
    #code 분류 100 정치 101 경제 102 사회 103 생활/문화 104 세계 105 IT/과학
    for list in MAIN_CATEGORY:
        URL_LIST.append(BASE_URL+list)

    return URL_LIST

def getSubCategoryUrl(MainCategoryUrl, dateList):
    URL_LIST = []

    for mainUrl in MainCategoryUrl:
        soup = getsoup(mainUrl)

        #각 page의 뉴스를 news_list에 저장
        news_list = soup.select('.massmedia li')
        news_list.extend(soup.select('.massmedia li'))
        print(news_list)
        #page에 있는 뉴스 주소를 가져와 url_list에 append
        for line in news_list:
            URL_LIST.append(line.a.get('href'))
        
    return URL_LIST
#main url, sub url, date

if __name__ == "__main__":
    dateList = getDateRange()

    MainCategoryUrl = getMainCategoryUrl()
    SubCategoryUrl = getSubCategoryUrl(MainCategoryUrl, dateList)
    print(SubCategoryUrl)