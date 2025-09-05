a = 1
def vartest(a):  # 매개변수 a는 지역(local) 변수(with 매개변수)
    print(a)     # 1 출력
    a = a + 1
    print(a)     # 2 출력

vartest(a)       # vartest(1)과 동일
print(a)         # 1 출력