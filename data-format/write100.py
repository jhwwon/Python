# 바이너리 파일 생성
# 파일 이름과 데이터
filename = "a.bin"
data = [11,12,13,14,5]
data1 = 'abcd'

# 쓰기
with open(filename, "wb") as f:
    # f.write(bytearray(data))
    f.write(bytearray([11,12,13,14,5]))   # 11(10진수) -> 0B(16진수)  12 -> 0B   13 -> 0C
    # f.write(bytes(data))
    # f.write(data1)

