import itertools
students = ['홍길동', '이순신', '강감찬', '김유신']
snacks = ['쿠키', '사탕', '초콜릿']

result = itertools.zip_longest(students, snacks, fillvalue='과자')
print(list(result))