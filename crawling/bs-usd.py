from bs4 import BeautifulSoup
import urllib.request as req

# HTML 가져오기
url = "http://finance.naver.com/marketindex/"
res = req.urlopen(url)

# HTML 분석하기
soup = BeautifulSoup(res, "html.parser")
# 원하는 데이터 추출하기 --- (※1)
#price = soup.select_one("div.head_info > span.value").string
price = soup.select_one("#exchangeList > li.on > a.head.usd > div > span.value").string
print("usd/krw =", price)

# WTI 값 
price2 = soup.select_one("#oilGoldList > li.on > a.head.wti > div > span.value").string
print("WTI 값 =", price2)
