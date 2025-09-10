import urllib.request 

# URL과 저장 경로 지정하기
url = "http://uta.pw/shodou/img/28/214.png"
savename = "test.png"

# 다운로드 --- (※1)
mem = urllib.request.urlopen(url).read()  # get방식으로 가지고 오고 바이너리(binary) 데이터로 변수에 저장

# 파일로 저장하기 --- (※2)
with open(savename, mode="wb") as f:
    f.write(mem)
    print("저장되었습니다...!")