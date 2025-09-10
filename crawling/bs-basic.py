from bs4 import BeautifulSoup

soup = BeautifulSoup(
  '<html><body><ul><li><a href="http://www.naver.com" class="test1" id="">naver</a></li></ul></body></html>'
  , 'html.parser'
  )
#print(soup.prettify())   # html소스 가독성 좋게 출력

a_list = soup.find_all('a')
for a in a_list:
  #if a.attrs['target']:   # 내부 error(try문 사용하여 handling)
  if 'target' in a.attrs:   # a태그 안의 target의 속성값이 있다면(empty포함)
    print(a.attrs['target'])
