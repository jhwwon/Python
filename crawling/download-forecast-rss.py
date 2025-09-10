import urllib.request
import urllib.parse

API = "https://www.kma.go.kr/repositary/xml/fct/mon/img/fct_mon3rss_108_20250822.xml"  # rss xml파일


# 다운로드합니다. --- (※3)
data = urllib.request.urlopen(API).read()
text = data.decode("utf-8")
print(text)