prompt = """
... 1. Add
... 2. Del
... 3. List
... 4. Quit
...
... Enter number: """

number = 0
while number != 4:
    print(prompt)
    number = int(input()) #input()함수는 문자열을 반환하므로 int()로 감싸서 정수로 변환