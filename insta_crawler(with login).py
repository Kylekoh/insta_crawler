# -*- encoding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import pandas as pd


baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome()
driver.get(url)

time.sleep(2)

# 로그인 하기(아이디, 패스워드 입력)
login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
driver.find_element_by_xpath(login_section).click()
time.sleep(3)
elem_username = driver.find_element_by_name('username')
elem_username.clear()
elem_username.send_keys('ko12ztwe@gmail.com')
time.sleep(1)
elem_password = driver.find_element_by_name('password')
elem_password.clear()
elem_password.send_keys('merch0824!')
time.sleep(1.5)
# 로그인 하기(로그인 버튼 클릭)
login_button = '//*[@id="loginForm"]/div/div[3]/button'
driver.find_element_by_xpath(login_button).click()

time.sleep(2)

# 검색페이지 접속하기
driver.get(url)
time.sleep(2)


imgList = []
reallink = []
for i in range(0, 5):
    posts = driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w")
    # print(posts)

    for post in posts:
        # print(post)
        # imgUrl = i.select_one('.KL4Bh').img['src']
        # imgList.append(imgUrl)
        # imgList = list(set(imgList))
        # print(post)

        temp = post.get_attribute('innerHTML')
        soup = BeautifulSoup(temp, 'lxml')
        link = soup.find('a', href=True)['href']
        print(link)

        # 포스팅마다 hover를 해서 좋아요(조회수), 댓글수를 가지고 온다
        hover = ActionChains(driver).move_to_element(post).perform()

        html = driver.find_elements(
            By.CLASS_NAME, "qn-0x")[0].get_attribute('innerHTML')

        soup = BeautifulSoup(html, 'lxml')
        elements = soup.findAll(attrs={'class': '-V_eO'})

        if len(elements) == 2:
            like = elements[0].find('span').text
            comments = elements[1].find('span').text
        elif len(elements) == 1:
            like = '0'
            comments = elements[0].find('span').text

        if int(like.replace(',', '')) + int(comments.replace(',', '')) > 50:
            reallink.append(link)
            # print(link)
            # print(like)
            # print(comments)
            # print('########')

        posts = driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w")
        print(posts)
        time.sleep(1)

    print("스크롤 !!!!!")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)


print(reallink)


# 로드된 모든 포스트를 가지고 온다
# posts = driver.find_elements_by_css_selector(".v1Nh3.kIKUG._bz0w")
# print(posts)


# print(insta)

SCROLL_PAUSE_TIME = 1.2
reallink = []


# for post in posts:
#     temp = post.get_attribute('innerHTML')
#     soup = BeautifulSoup(temp, 'lxml')
#     link = soup.find('a', href=True)['href']

#     # 포스팅마다 hover를 해서 좋아요(조회수), 댓글수를 가지고 온다
#     hover = ActionChains(driver).move_to_element(post).perform()

#     html = driver.find_elements(
#         By.CLASS_NAME, "qn-0x")[0].get_attribute('innerHTML')

#     soup = BeautifulSoup(html, 'lxml')
#     elements = soup.findAll(attrs={'class': '-V_eO'})

#     if len(elements) == 2:
#         like = elements[0].find('span').text
#         comments = elements[1].find('span').text
#     elif len(elements) == 1:
#         like = 0
#         comments = elements[0].find('span').text

#     if int(like) + int(comments) > 50:

#         reallink.append(link)
#         print(link)
#         print(like)
#         print(comments)
#         print('########')

#     time.sleep(1)

# for i in range(0, len(reallink)):
#     # for i in range(0, 1):
#     req = 'https://www.instagram.com'+reallink[i]
#     driver.get(req)
#     webpage = driver.page_source
#     soup = BeautifulSoup(webpage, 'html.parser')

#     # 포스팅 종류
#     # 썸네일(사진 or 동영상)
#     if soup.find(attrs={'class': 'tWeCl'}) == None:
#         postType = '사진'
#         thumbNail = soup.find(attrs={'class': 'FFVAD'})['src']

#     else:
#         postType = '영상'
#         thumbNail = soup.find(attrs={'class': '_8jZFn'})['src']

#     # 좋아요 // 조회수
#     # 좋아요가 없는 경우 0으로처리
#     if soup.find(attrs={'class': 'vcOH2'}):
#         try:
#             view = soup.find(attrs={'class': 'vcOH2'}).find('span').text
#         except:
#             view = 0
#         like = 'X'
#     else:
#         view = 'X'
#         try:
#             like = soup.find(
#                 attrs={'class': 'sqdOP yWX7d _8A5w5'}).find('span').text
#         except:
#             like = 0

#     # 유저 이미지
#     userImage = soup.find(attrs={'class': '_6q-tv'})['src']

#     # 유저 아이디
#     userId = soup.find_all(attrs={'class': 'sqdOP yWX7d _8A5w5 ZIAjV'})[0].text
#     # 내용
#     content = soup.find(attrs={'class': 'C4VMK'}).find('span').text

#     a = [[req, thumbNail, userImage, postType, userId, content, like, view]]
#     final_df = pd.DataFrame(
#         a, columns=['게시물 링크', '썸네일', 'User이미지', '포스팅 종류', 'User ID', '내용', '좋아요', '조회수'])
#     # header를 처음 1번만 써주기 위해서 구분해준다
#     if i == 9:
#         final_df.to_csv('인스타 크롤링 결과(공구).csv', index=False,
#                         mode='a', encoding="utf-8-sig")
#     else:
#         final_df.to_csv('인스타 크롤링 결과(공구).csv', index=False, mode='a',
#                         header=False, encoding="utf-8-sig")

#     print(req)
#     print()
#     print(thumbNail)
#     print()
#     print(userImage)
#     print()
#     print(userId)
#     print()
#     print(content)
#     print()
#     print(like)
#     print('#########################')
#     time.sleep(2)

time.sleep(1)
driver.close()


# 스크롤링
# while True:
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#         time.sleep(SCROLL_PAUSE_TIME)
#         new_height = driver.execute_script('return document.body.scrollHeight')
#         if new_height == last_height:
#             break
#         else:
#             last_height = new_height
#             continue
