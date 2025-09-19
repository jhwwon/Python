import json
import urllib.request as req
import os.path, random

# 1. JSON 데이터 내려받기(urlopen 혹은 urlretrieve 사용)
url = "https://api.github.com/repositories"
savename = "repo.json"

if not os.path.exists(savename): # repo.json 파일이 없으면
    req.urlretrieve(url, savename)

# 2. string으로 된 json notation을 파이썬 json 객체 저장
# json.loads()   : string(json) -> object(json)
items = json.loads(open(savename, "r", encoding="utf-8"))

# items -: [ { }, { }, { } ]
for item in items:
    print(item["name"] + " - " + item["owner"]["login"])