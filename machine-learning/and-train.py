from sklearn import svm  # 지도 학습에 사용되는 svm알고리즘

# AND의 계산 정답 결과 훈련 데이터
and_data = [
    #P, Q, R(결과)
    [0, 0, 0],
    [0, 1, 0],
    [1, 0, 0],
    [1, 1, 1],
]

data = []   # 학습 데이터
label = []  # 레이블 데이터
for row in and_data:
    data.append([row[0], row[1]])   # 학습 데이터(P, Q)
    label.append(row[2])            # 레이블 데이터(R(결과))

# SVM 지도 학습 알고리즘으로 학습
clf = svm.SVC()      # svm학습 객체 저장
clf.fit(data, label) # fit을 통해서 학습

# 데이터 정답 예측 모델
pre = clf.predict(data)
print("예측결과:", pre)

test_data = [1,0,0,0]   # 문제 테스트 데이터
ok = 0; total = 0
for idx, answer in enumerate(test_data):
    p = pre[idx]
    if p == answer: ok += 1
    total += 1

print('정답률:', ok, "/", total, "=", ok / total)