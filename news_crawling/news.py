from cgitb import text
from email import header
from msilib.schema import TextStyle
import requests, re
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def getsoup(url): #BeautifulSoup를 사용해 HTML 분석
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Whale/3.12.129.46 Safari/537.36'}
    res = requests.get(url, headers=headers)
    return BeautifulSoup(res.content, 'html.parser')

def get_url(pg_num, code, date): #크롤링 할 뉴스 URL리스트 받기
    urllist = []

    for i in range(1, pg_num +1):
        url = 'https://news.naver.com/main/list.nhn?mode=LSD&mid=sec&sid1='+code+'&date='+date+'&page='+str(i)
        html = getsoup(url)

        #각 page의 뉴스를 news_list에 저장
        news_list = html.select('.type06_headline li dl')
        news_list.extend(html.select('.type06 li dl'))

        #page에 있는 뉴스 주소를 가져와 url_list에 append
        for line in news_list:
            urllist.append(line.a.get('href'))
    return urllist

def isHangeul(text):
    #Unicode로 한글 길이 측정
    han_cnt = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', text))
    if han_cnt > 0:
        return True
    else:
        return False

def get_post(url): #뉴스 본문 크롤링
    html = getsoup(url)

    #뉴스 본문 가져오기
    div = html.find("div", class_="go_trans _article_content")
    #뉴스 요약 삭제하기
    text = re.sub('<strong.*?>.*?</strong>', '', str(div))
    #HTML tag 삭제하기
    text = re.sub('(<([^>]+)>)', '', str(text))
    #개행문자, 탭, 백슬래시 제거하기
    text = text.replace("\n","").replace("\t","").replace('\\','')
    #한글 기사인지 확인하기
    if isHangeul(text) == False:
        return 

    return text

def main():
    page_num = 1
    code = '001' #code 분류 001 전체 100 정치 101 경제 102 사회 103 생활/문화 104 세계 105 IT/과학
    date = datetime.strftime(datetime.today(),'%Y%m%d') #오늘 날짜 받기

    #각 기사의 url 받아오기
    url_list = []
    url_list = get_url(page_num,code,date)
    #print(url_list)

    #받아온 url에 해당하는 기사의 본문 받아오기
    post_list = []
    for url in url_list:
        post_list.append(get_post(url))

    #dataframe에 500길이까지 print할 수 있는 명령
    pd.options.display.max_colwidth = 1500
    data = pd.DataFrame({"URL": list(url_list), "TEXT": list(post_list)})
    print(data)


main()

#https://joon0zo.tistory.com/20