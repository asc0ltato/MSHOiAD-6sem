# В подходе «один против остальных» для каждого класса строится бинарная
# модель, которая пытается отделить этот класс от всех остальных, в
# результате чего количество моделей определяется количеством классов.
# Классификатор, который выдает по своему классу наибольшее значение,
# «побеждает» и метка этого класса возвращается в качестве прогноза.
import mglearn
import sklearn
import matplotlib.pyplot as plt
import numpy as np

# используется двумерный массив, где каждый класс задается данными,
# а эти данные в свою очередь берутся из распределения гаусса
from sklearn.datasets import make_blobs
X, y = make_blobs(random_state=42)
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.legend(["Класс 0", "Класс 1", "Класс 2"])
plt.show()

# Обучаем LinearSVC на нашем наборе данных
# (3,2) - каждая строка coef_ содержит w для каждого из трех классов, а
# каждый столбец содержит w для конкретного признака (тут их 2).
# (3,) - сколько смещений
from sklearn.svm import LinearSVC
linear_svm = LinearSVC(dual=True).fit(X, y)
print("Форма коэффициента: ", linear_svm.coef_.shape)
print("Форма константы: ", linear_svm.intercept_.shape)
# intercept_ - этот атрибут теперь одномерный массив (тут константы классов)

# Визуализируем линии (границы принятия решений)

# Точки класса 0 выше линии для класса 0, что относит их к этому классу.
# Они также выше линии для класса 2 и слева от линии для класса 1,
# что классифицирует их как «остальные».
# Таким образом, любая точка в этой области будет отнесена к классу 0,
# так как его значение больше нуля.
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
line = np.linspace(-15, 15)
for coef, intercept, color in zip(linear_svm.coef_, linear_svm.intercept_, ['b', 'r', 'g']):
    plt.plot(line, -(line * coef[0] + intercept) / coef[1], c=color)
plt.ylim(-10, 15)
plt.xlim(-10, 8)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.legend(['Класс 0', 'Класс 1', 'Класс 2', 'Линия класса 0', 'Линия класса 1', 'Линия класса 2'], loc=(1.01, 0.3))
plt.show()

# показывает прогнозы для всех областей двумерного пространства
mglearn.plots.plot_2d_classification(linear_svm, X, fill=True, alpha=.7)
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
line = np.linspace(-15, 15)
for coef, intercept, color in zip(linear_svm.coef_, linear_svm.intercept_, ['b', 'r', 'g']):
    plt.plot(line, -(line * coef[0] + intercept) / coef[1], c=color)
plt.legend(['Класс 0', 'Класс 1', 'Класс 2', 'Линия класса 0', 'Линия класса 1', 'Линия класса 2'], loc=(1.01, 0.3))
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()