from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings
import urllib.request as req

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

url = "https://www.kma.go.kr/repositary/xml/fct/mon/img/fct_mon3rss_108_20250822.xml"
# urlopen()으로 데이터 가져오기 --- (※1)
res = req.urlopen(url)

# BeautifulSoup으로 분석하기 --- (※2)
soup = BeautifulSoup(res, "html.parser")

# 원하는 데이터 추출하기 --- (※3)
title = soup.find("title")
print(type(title))
# wf = soup.find("wf").string  # xml로 된 wf태그가 없어서 error
summary = soup.find("summary").get_text()

title_list = soup.find_all("title")
print(type(title_list))

print(title.get_text())
#print(wf)
print(summary)