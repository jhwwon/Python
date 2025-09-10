from bs4 import BeautifulSoup 

html = """
<html>
  <body>
    <ul>
      <li><a href="http://www.naver.com" class="test1" id="" target="">naver</a></li>
      <li><a href="http://www.daum.net">daum</a></li>
    </ul>
  </body>
</html>
"""

# HTML 분석하기 --- (※1)
soup = BeautifulSoup(html, 'html.parser')

# find_all() 메서드로 추출하기 --- (※2)
links = soup.find_all("a")

# 링크 목록 출력하기 --- (※3)
for a in links:
    href = a.attrs['href']  # a태그의 href속성의 값
    
    try:
      print(a.attrs['class'])
    except:
       print('class속성이 없음')
    # print(type(a.attrs['class']))
    # print(a.attrs['class'])  # ['test1'] 만약 속성이 없는 경우이면 keyerror
    # print(a.attrs['class'][0])  # test1

    text = a.string
    print(text, ">", href)