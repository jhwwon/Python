# 로그인을 위한 모듈 추출하기
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 아이디와 비밀번호 지정하기[자신의 것을 사용해주세요] --- (※1)
USER = ""
PASS = "jhwwaterm1270!!"

# 세션 시작하기 --- (※2)
session = requests.session()

# 추가할 헤더를 딕셔너리로 정의
custom_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "Authorization": "Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbklkIjoicGt0amVzdXMxIiwibWVtYmVySWQiOjI3MDkwNCwiYXV0aCI6IlJPTEVfTUVNQkVSLFJPTEVfUFJPRkVTU09SX0JBU0lDIiwiaWF0IjoxNzU3NTU1NjgxLCJleHAiOjE3NTc1NzcyODF9.6ch4RSoNQdZ_fQCVaCzqJfd6QopPn_EthFUHDjLNAVgDaIuZrBamkHp10M5rHWX2Ub9Tdr9WmtGf35hQlnm3Mg"
}
# Session 객체의 headers에 추가
session.headers.update(custom_headers)

# 로그인하기 --- (※3)
login_info = {
    "id": USER,     # 아이디 지정
    "password": PASS  # 비밀번호 지정
}
url_login = "https://www.hanbit.co.kr/login"
res = session.post(url_login, data=login_info)
res.raise_for_status() # 오류가 발생하면 예외가 발생합니다.
print(res.text)


# # 마이페이지에 접근하기 --- (※4)
# url_mypage = "https://www.hanbit.co.kr/myhanbit/myhanbit.html"
# res = session.get(url_mypage)
# res.raise_for_status()

# # 마일리지와 이코인 가져오기 --- (※5)
# soup = BeautifulSoup(res.text, "html.parser")
# mileage = soup.select_one("#container > div > div.sm_mymileage > dl.mileage_section1 > dd > span").get_text()
# ecoin = soup.select_one("#container > div > div.sm_mymileage > dl.mileage_section2 > dd > span").get_text()

# print("마일리지: " + mileage)
# print("이코인: " + ecoin)