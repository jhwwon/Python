import urllib.request
import urllib.parse
import sys

# 명령줄 매개변수 추출
if len(sys.argv) <= 1:
    print("사용법: python download-kyobobook-param.py 찾고싶은책이름")
    sys.exit() # 프로그램 중단
search_keyword = sys.argv[1]

API = "https://search.kyobobook.co.kr/search"
# 매개변수를 URL 인코딩합니다. --- (※1)
values = {
    'keyword': search_keyword,
    'gbCode': 'TOT',
    'target': 'total',
}
params = urllib.parse.urlencode(values)

# 요청 전용 URL을 생성합니다. --- (※2)
url = API + '?' + params
print("url=", url)

# Header 설정
headers = {
    "User-Agent": "User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",  # 사용자 브라우저에서 실행한 것처럼 설정1
}

# header 포함 요청 객체 생성
req = urllib.request.Request(url, headers=headers)

# 다운로드합니다. --- (※3)
data = urllib.request.urlopen(req).read()
text = data.decode("utf-8")
print(text)
