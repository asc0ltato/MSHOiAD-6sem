import pandas as pds
import mglearn
import matplotlib.pyplot as plt
import numpy as np

from sklearn.datasets import load_iris
iris_dataset = load_iris()

# X - данные, y - метки (сорт, к которому принадлежит цветок(это точка данных))
# X_train - в обучающий набор 75% строк данных с соответствующими метками
# X_test - 25% - тестовый набор
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
iris_dataset['data'], iris_dataset['target'], random_state=0)

print("форма массива X_train: {}".format(X_train.shape)) # обучающие данные
print("форма массива y_train: {}".format(y_train.shape)) # обучающие метки
print("форма массива X_test: {}".format(X_test.shape))
print("форма массива y_test: {}".format(y_test.shape))

# Кол-во соседей 1
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors=1)

# построение модели на обучающем наборе
knn.fit(X_train, y_train)

# новые данные
X_new = np.array([[5, 2.9, 1, 0.2]])
# примеры * кол-во признаков
print("форма массива X_new: {}".format(X_new.shape))

# делаем прогноз для нового набора и тестового
prediction = knn.predict(X_new)
print("Прогноз: {}".format(prediction)) # к классу 0
print("Спрогнозированная метка: {}".format(iris_dataset['target_names'][prediction])) # сорт setosa
y_pred = knn.predict(X_test)
print("Прогнозы для тестового набора:\n {}".format(y_pred))

# mean, score - вычисление правильности модели для тестового набора
print("Правильность на тестовом наборе: {:.2f}".format(np.mean(y_pred == y_test)))
print("Правильность на тестовом наборе: {:.2f}".format(knn.score(X_test, y_test)))