from faker import Faker
fake = Faker('ko_KR')   # 한국어 설정

for _ in range(5):
    print(fake.name())
    print(fake.address())

test_data = [(fake.name(), fake.address()) for i in range(30)]
print(test_data)