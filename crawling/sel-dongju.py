from bs4 import BeautifulSoup 
import urllib.request

# 뒤의 인코딩 부분은 "저자:윤동주"라는 의미입니다.
# 따로 입력하지 말고 위키 문헌 홈페이지에 들어간 뒤에 주소를 복사해서 사용하세요.
url = "https://ko.wikisource.org/wiki/%EC%A0%80%EC%9E%90:%EC%9C%A4%EB%8F%99%EC%A3%BC"
# Header 설정
headers = {
    "User-Agent": "User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",  # 사용자 브라우저에서 실행한 것처럼 설정1
}

# header 포함 요청 객체 생성
req = urllib.request.Request(url, headers=headers)
data = urllib.request.urlopen(req)
# print('data', data)
soup = BeautifulSoup(data, "html.parser")

# #mw-content-text 바로 아래에 있는 
# ul 태그 바로 아래에 있는
# li 태그 아래에 있는
a_list = soup.select("#mw-content-text > div.mw-content-ltr.mw-parser-output ul:nth-child(8) > li > a")
print(a_list)
for a in a_list:
    name = a.string
    print("-", name)


