# calculator3.py
class Calculator:
    def __init__(self):   # 생성자 (생성자는 만들어주는게 좋음 밑줄 2개)
        self.result = 0
        print("초기화 완료")

    def add(self, num):   # 함수(메소드)
        self.result += num
        return self.result

cal1 = Calculator()   # 객체 생성(java에서는 new Calculator())
cal2 = Calculator()

print(cal1.add(3))
print(cal1.add(4))
print(cal2.add(3))
print(cal2.add(7))