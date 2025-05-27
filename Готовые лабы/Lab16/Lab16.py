# тестируем три разных Наивных Байесовских классификатора
import mglearn
import sklearn
import matplotlib.pyplot as plt
import numpy as np
from sklearn.naive_bayes import BernoulliNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB

# Классификатор BernoulliNB
# матрица признаков (строка - точка (4 - количество признаков))
X = np.array([[0, 1, 0, 1], [1, 0, 1, 1], [0, 0, 0, 1], [1, 0, 1, 0]])
y = np.array([0, 1, 0, 1])
counts = {}
for label in np.unique(y):
 counts[label] = X[y == label].sum(axis=0) # сколько раз встречается
print("Частоты признаков:\n{}".format(counts))
clf = BernoulliNB()
clf.fit(X, y)
clfp = clf.predict(X[2:3])
print("clf.predict:\n{}".format(clfp))

# Классификатор MultinomialNB
# Частоты появления признаков
rng = np.random.RandomState(1) # случ числа будут одинаковыми
# матрица признаков (строка - точка (100 - количество признаков))
X = rng.randint(5, size=(6, 100))
y = np.array([1, 2, 3, 4, 5, 6]) # классы
clf = MultinomialNB()
clf.fit(X, y)
print(clf.predict(X[2:3])) # прогноз для 3 строки

# Классификатор GaussianNB
# Непрерывные признаки, нормальное распределение
# матрица признаков (строка - точка (каждая с 2 признаками))
X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
Y = np.array([1, 1, 1, 2, 2, 2]) # 3 точки 1 классу и 2 классу
clf = GaussianNB()
clf.fit(X, Y)
print(clf.predict([[-0.8, -1]])) # предсказываем
clf_pf = GaussianNB()
clf_pf.partial_fit(X, Y, np.unique(Y)) # список всех возможных классов
print(clf_pf.predict([[-0.8, -1]]))