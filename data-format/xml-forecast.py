# 3개월 전망을 표시하는 코드 실습 예제

from bs4 import BeautifulSoup
import urllib.request as req
import os.path

savename = "forecast.xml"
if not os.path.exists(savename):
    print('forecast.xml파일이 없습니다.')

url = "https://www.kma.go.kr/repositary/xml/fct/mon/img/fct_mon1rss_108_20250911.xml"
# url 요청해서 응답한 값을 savename변수에 넣기
req.urlretrieve(url, savename)
# savename변수의 텍스트 내용을 xml변수에 넣기
xml = open(savename, "r", encoding="utf-8").read()

soup = BeautifulSoup(xml, "html.parser")

# 일자별 날씨 현황 확인하기
info = {}  # 원하는 형식대로 json으로 데이터 구조 저장할 변수
# print(soup.find_all("week"))
for week in soup.find_all("week"):
    # 날씨 기간
    period = week.find(lambda tag: tag.name.endswith('period')).get_text()
    # 날씨 기간에 대한 정보
    weather_review = week.find(lambda tag: tag.name.endswith('weather_review')).get_text()
    
    # 원하는 형식대로 담은 변수에 필요한 데이터 저장
    if not (weather_review in info):
        info[period] = []       # 값이 중복된 게 있으면 초기화
    info[period].append(weather_review)

# 각 일자의 날씨 정보를 구분해서 출력하기
for period in info.keys():
    print("+", period)
    for name in info[period]:
        print("| - ", name)