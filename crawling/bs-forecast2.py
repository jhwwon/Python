from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
import urllib.request as req

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

url = "https://www.kma.go.kr/repositary/xml/fct/mon/img/fct_mon1rss_108_20250904.xml"

# urlopen()으로 데이터 가져오기 --- (※1)
res = req.urlopen(url)

# BeautifulSoup으로 분석하기 --- (※2)
soup = BeautifulSoup(res, "html.parser")

# 원하는 데이터 추출하기 --- (※3)
title = soup.find("title")
print(type(title))

# week1_weather_review 태그를 찾아서 텍스트 내용 추출
week1_weather = soup.find("week1_weather_review")
if week1_weather:
    week1_text = week1_weather.get_text()
    print("1주차 날씨 전망:")
    print(week1_text)
else:
    print("week1_weather_review 태그를 찾을 수 없습니다")

summary = soup.find("summary").get_text()

title_list = soup.find_all("title")
print(type(title_list))

print(title.get_text())
print(summary)