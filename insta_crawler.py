# -*- encoding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import pandas as pd
from pymongo import MongoClient


keyword_list = ['공구', '공구마켓', '공동구매', '공구오픈', '공구중']


for keyword in keyword_list:
    event_hashtag = keyword
    print('###################')
    print(event_hashtag)
    print('###################')
    baseUrl = 'https://www.instagram.com/explore/tags/'
    url = baseUrl + quote_plus(keyword)

    driver = webdriver.Chrome()
    driver.get(url)

    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".v1Nh3.kIKUG._bz0w"))
        )

    except Exception as E:
        print(E)
        driver.quit()
        continue

    time.sleep(2)

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    linkList = []
    reallink = []

    # 검색 결과 화면 스크롤링, 횟수 조절(7회)
    for i in range(0, 7):
        insta = soup.select('.v1Nh3.kIKUG._bz0w')

        for i in insta:
            postUrl = i.a['href']
            linkList.append(postUrl)
            # 링크 중복제거
            for v in linkList:
                if v not in reallink:
                    reallink.append(v)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            insta = soup.select('.v1Nh3.kIKUG._bz0w')

        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

    n = 0
    for i in range(9, len(reallink)):
        event_permlink = 'https://www.instagram.com'+reallink[i]
        driver.get(event_permlink)
        webpage = driver.page_source
        soup = BeautifulSoup(webpage, 'html.parser')

        # 좋아요, 조회수
        # 좋아요, 조회수가 없는 경우 0으로처리
        if soup.find(attrs={'class': 'vcOH2'}):
            try:
                event_views = soup.find(
                    attrs={'class': 'vcOH2'}).find('span').text
            except:
                event_views = '0'
            event_likes = '0'
        else:
            event_views = '0'
            try:
                event_likes = soup.find(
                    attrs={'class': 'sqdOP yWX7d _8A5w5'}).find('span').text
            except:
                event_likes = '0'

        # 영상 게시물 조회수 80 이하, 사진 게시물 좋아요 40 이하라면 다음 절차 skip
        if int(event_views.replace(',', '')) >= 80 or int(event_likes.replace(',', '')) >= 40:
            n += 1
            if soup.find(attrs={'class': 'tWeCl'}) == None:
                postType = '사진'
                event_media_url = soup.find(attrs={'class': 'FFVAD'})['src']

            else:
                postType = '영상'
                try:
                    event_media_url = soup.find(
                        attrs={'class': '_8jZFn'})['src']
                except:
                    event_media_url = soup.find(
                        attrs={'class': 'tWeCl'})['src']

            # 유저 이미지
            event_user_url = soup.find(attrs={'class': '_6q-tv'})['src']

            # 유저 아이디
            event_username = soup.find_all(
                attrs={'class': 'sqdOP yWX7d _8A5w5 ZIAjV'})[0].text
            # 내용
            event_caption = soup.find(
                attrs={'class': 'C4VMK'}).find('span').text

            # 포스트 생성일자
            event_timestamp = soup.find(
                attrs={'class': '_1o9PC Nzb55'})['datetime']

            # mongoDB에 데이터 저장
            # datum = {}
            # datum['event_hashtag'] = event_hashtag
            # datum['event_permlink'] = event_permlink
            # datum['event_media_url'] = event_media_url
            # datum['event_user_url'] = event_user_url
            # datum['event_timestamp'] = event_timestamp
            # datum['event_username'] = event_username
            # datum['event_caption'] = event_caption
            # datum['event_likes'] = int(event_likes.replace(',', ''))
            # datum['event_views'] = int(event_views.replace(',', ''))

            # username = quote_plus('dev')
            # password = quote_plus('qpalzm!!05')

            # client = MongoClient(
            #     "mongodb://%s:%s@54.183.115.146:27017" % (username, password))
            # mydb = client["crawled"]
            # mycol = mydb["insta"]
            # mycol.insert_one(datum)

            # client = MongoClient(
            #     "mongodb://localhost:27017")
            # mydb = client["insta"]
            # mycol = mydb["posts"]
            # mycol.insert_one(datum)

            a = [[event_hashtag, event_permlink, event_media_url, event_user_url, event_timestamp,
                  postType, event_username, event_caption, event_likes, event_views]]

            final_df = pd.DataFrame(
                a, columns=['키워드', '게시물 링크', '썸네일URL', 'User이미지URL', '게시물 생성일', '포스팅 종류', 'User ID', '내용', '좋아요', '조회수'])

            # header(컬럼 네임)를 처음 1번만 써주기 위해서 구분
            date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            if n == 1:
                final_df.to_csv('인스타 리스트(%s).csv' % (date), index=False,
                                mode='a', encoding="utf-8-sig")
            else:
                final_df.to_csv('인스타 리스트(%s).csv' % (date), index=False, mode='a',
                                header=False, encoding="utf-8-sig")
            print(event_hashtag)
            print()
            print(event_permlink)
            print()
            print(event_media_url)
            print()
            print(event_user_url)
            print()
            print(event_username)
            print()
            print(event_caption)
            print()
            print(event_likes)
            print()
            print(event_views)
            print('#################################################')
            time.sleep(2)
        else:
            continue

    time.sleep(1)
    driver.close()∑