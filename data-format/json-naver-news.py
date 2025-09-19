import json
import urllib.request as req
import urllib.parse

# 1. JSON 데이터 내려받기(urlopen 혹은 urlretrieve 사용)
# 한글을 해석할 수 있도록 encode
encode_data = urllib.parse.quote_plus('대통령')  # 한글 처리
url = "https://openapi.naver.com/v1/search/news.json?query=" + encode_data

# savename = "naver-news.json"
# 2. Request 객체 생성 및 헤더 추가 
req1 = req.Request(url)
req1.add_header('X-Naver-Client-Id', 'Z5zWnTnOT0M66TM4_sY4')
req1.add_header('X-Naver-Client-Secret', 'v_Xqi0BvUU')
req1.add_header("Content-Type", "application/json")

# 3. 요청 실행
with req.urlopen(req1) as response:
    # 4. string으로 된 json notation을 파이썬 json 객체 저장
    # json.loads()   : string(json) -> object(json)
    # test1 = response.read().decode('utf-8'))
    # print(type())    # string(json)
    items = json.loads(response.read().decode('utf-8'))     
    print(type(items))                              # object(dict)(json)

    count = 0
    for item in items["items"]:
        count += 1
        print('title:', item["title"])

    print(count)

