import json

# 변수 객체(json)
price = {
    "date": "2017-05-10",
    "price": {
        "Apple": 80,
        "Orange": 55,
        "Banana": 40
    }
}
print('original type', type(price))

# 변수 객체(json) -> String(json)
s = json.dumps(price)
print('dumps type', type(s))
print(s)

