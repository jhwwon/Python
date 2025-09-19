from sklearn import svm, metrics
import random, re

# 붓꽃의 CSV 데이터 읽어 들이기
iris_csv = []
with open('./machine-learning/iris.csv', 'r', encoding='utf-8') as fp:
    # 한 줄씩 읽어 들이기
    for line in fp:
        line = line.strip()    # 줄바꿈 제거
        cols = line.split(',') # 쉼표로 자르기
        # 문자열 데이터를 숫자로 변환하기
        fn = lambda n : float(n) if re.match(r'^[0-9\.]+$', n) else n
        cols = list(map(fn, cols))
        iris_csv.append(cols)

del iris_csv[0]  # 앞 첫째 줄 제거
print(iris_csv)

random.shuffle(iris_csv)  # 학습을 더 잘하기 위한 용도도 훈련 데이터를 셔플(옵션)

# 학습(훈련) 데이터와 테스트 데이터를 분할하기(2:1)
total_len = len(iris_csv)           # 150
train_len = int(total_len * 2 / 3)  # 100

train_data = []
train_label= []
test_data = []
test_label= []
for i in range(total_len):
    data = iris_csv[i][0:3]
    label = iris_csv[i][4]
    # 앞의 100까지는 훈련 데이터, 101부터는 테스트 데이터
    if i < train_len:
        train_data.append(data)
        train_label.append(label)
    else:
        test_data.append(data)
        test_label.append(label)

# 데이터 학습과 예측하기
clf = svm.SVC()
clf.fit(train_data, train_label)
pre = clf.predict(test_data)

# 정답률 구하기
ac_score = metrics.accuracy_score(test_label, pre)
print("정답률 =", ac_score)