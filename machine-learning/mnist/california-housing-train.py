import numpy as np
import pandas as pd
from sklearn import datasets
#
from sklearn import model_selection
from sklearn.svm import SVR
from sklearn import metrics

from sklearn import datasets
dataset = datasets.fetch_california_housing()
x_data = dataset.data
y_data = dataset.target
#print(x_data.shape) #(20640, 8)
#print(y_data.shape) #(20640,)

####################

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
scaler.fit(x_data)
x_data = scaler.transform(x_data)

x_train, x_test, y_train, y_test = model_selection.train_test_split(x_data, y_data, test_size=0.3)

estimator = SVR(kernel='rbf', C=1.0, gamma='auto')

estimator.fit(x_train, y_train)

y_predict = estimator.predict(x_train) 
score = metrics.r2_score(y_train, y_predict)
print(score) #1.0

y_predict = estimator.predict(x_test) 
score = metrics.r2_score(y_test, y_predict)
print(score) #1.0