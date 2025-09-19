import pandas as pd
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split

# 데이터 프레임으로 붓꽃의 CSV데이터 읽어오기
iris_csv = pd.read_csv("./machine-learning/iris.csv")
iris_csv_data = iris_csv[["SepalLength", "SepalWidth", "PetalLength", "PetalWidth"]]
iris_csv_label = iris_csv["Name"]

# 학습 및 테스트 전용 데이터 나누기
train_data, test_data, train_label, test_label \
    = train_test_split(iris_csv_data, iris_csv_label)

# 데이터 학습과 예측하기
clf = svm.SVC()
clf.fit(train_data, train_label)
pre = clf.predict(test_data)

# 정답률 구하기
ac_score = metrics.accuracy_score(test_label, pre)
print("정답률 =", ac_score)

