# 데이터 가져오기
import requests

# PUT 방식으로 데이터 요청하기
r = requests.put("https://httpbin.org/put")
print(r.text)
# DELETE 방식으로 데이터 요청하기
r = requests.delete("https://httpbin.org/delete")
print(r.text)
# HEAD 방식으로 데이터 요청하기
r = requests.head("https://httpbin.org/get")
print(r.text)