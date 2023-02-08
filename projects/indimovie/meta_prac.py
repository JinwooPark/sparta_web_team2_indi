import requests
from bs4 import BeautifulSoup

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.dtryx.com/movie/list.do?cgid=FE8EF4D2-F22D-4802-A39A-D58F23A29C1E&Tab=indieart',headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

# body > div.content > div > div.movie-list.slider-type1
#> ul > li:nth-child(1) > div > a > div.info > div.subj
#> ul > li:nth-child(1) > div > a > div.img > img
#> ul > li:nth-child(1) > div > a > div.img > span
#> ul > li:nth-child(1) > div > a > div.info > div.etc
#> ul > li:nth-child(1) > div > a > div.info > div.actor
movies = soup.select('body > div.content > div > div.movie-list.slider-type1 > ul > li')

top10_count = 1
for movie in movies:
    a = movie.select_one('div > a > div.info > div.subj')
    if a is not None:
        title = a.text
        image = movie.select_one('div > a > div.img > img')['src']
        age = movie.select_one('div > a > div.img > span > i')['class']
        etc = movie.select_one('div > a > div.info > div.etc').text
        actor = movie.select_one('div > a > div.info > div.actor').text
        print(title, image, age, etc, actor)
    top10_count += 1
    if top10_count > 10:
        break

# 영화 이름 평점 관련 크롤링 코드
# import requests
# from bs4 import BeautifulSoup
#
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20230207',headers=headers)
#
# soup = BeautifulSoup(data.text, 'html.parser')
#
# #old_content > table > tbody > tr:nth-child(3) > td.title > div > a
# #old_content > table > tbody > tr:nth-child(4) > td.title > div > a
#
# movies = soup.select('#old_content > table > tbody > tr')
#
# for movie in movies:
#     a = movie.select_one('td.title > div > a')
#     if a is not None:
#         title = a.text
#         rank = movie.select_one('td:nth-child(1) > img')['alt']
#         star = movie.select_one('td.point').text
#         print(rank, title, star)
#

# 특정 영화 제목 이미지 설명 크롤링 코드
# import requests
# from bs4 import BeautifulSoup
#
# url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code=191597'
#
# headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
# data = requests.get(url,headers=headers)
#
# soup = BeautifulSoup(data.text, 'html.parser')
#
# title = soup.select_one('meta[property="og:title"]')['content']
# image = soup.select_one('meta[property="og:image"]')['content']
# desc = soup.select_one('meta[property="og:description"]')['content']
#
# print(title, image, desc)
# # 여기에 코딩을 해서 meta tag를 먼저 가져와보겠# 습니다.