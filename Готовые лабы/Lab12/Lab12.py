import sklearn
import mglearn
from mglearn.datasets import make_forge
import matplotlib.pyplot as plt
import numpy as np

print("---------------------------")

# набор данных forge выдуманный (содержит 2 признака)
X, y = make_forge()
# создаем диаграмму рассеивания
# каждая точка данных представлена в виде 1 маркера
# цвет и форма маркера указывает на класс, к которому принадлежит точка
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
plt.legend(["Класс 0", "Класс 1"], loc=4)
plt.xlabel("Первый признак")
plt.ylabel("Второй признак")
print("форма массива X: {}".format(X.shape)) # 26 точек данных и 2 признака
plt.show()

print("---------------------------")

# алгоритм регрессии - набор wave - синтетический набор
# имеет единственный входной признак (ось X) и непрерывную целевую
# переменную (отклик - response), который мы хотим смоделировать
X, y = mglearn.datasets.make_wave(n_samples=40)
plt.plot(X, y, 'o')
plt.ylim(-3, 3)
plt.xlabel("Признак")
plt.ylabel("Целевая переменная")
plt.show()

print("---------------------------")

# реальный набор по раку молочной железы, включает реальные измерения
# набор данных включает 569 точек данных и 30 признаков
# из них 212 как зло, 357 как добро
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
print("Ключи cancer(): \n{}".format(cancer.keys()))
print("Форма массива data для набора cancer: {}".format(cancer.data.shape))
print("Количество примеров для каждого класса:\n{}".format(
{n: v for n, v in zip(cancer.target_names, np.bincount(cancer.target))}))

print("---------------------------")

# 20640 точек и 8 признаков (приняты все взаимодействия между признаками)
# включение производных признаков - конструирование признаков
# алгоритм k = 1 и k = 3 ближайших соседа
# рассматривает лишь одного ближайшего соседа – точку обучающего набора,
# ближе всего расположенную к точке, для которой мы хотим получить прогноз
# прогнозом является ответ, уже известный для данной точки обучающего набора
# 3 новые точки данных (*), для каждой есть ближайшая точка обучающего набора
# прогноз - метка этой точки (цветом маркера)
from sklearn.datasets import fetch_california_housing
california = fetch_california_housing()
print("форма массива data для набора fetch_california_housing: {}".format(california.data.shape))
mglearn.plots.plot_knn_classification(n_neighbors=1)
plt.show()
mglearn.plots.plot_knn_classification(n_neighbors=3)
plt.show()

# набор данных с производными признаками (прогноз стоимости домов)
# 506 точек и 104 признака (в boston было 506 и 13, тут 91 производный
# признак)
X, y = mglearn.datasets.load_extended_boston()
print("форма массива X: {}".format(X.shape))

print("---------------------------")

# применение k ближайших соседей
from sklearn.model_selection import train_test_split
X, y = make_forge()
# делим данные на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
# используем 3 соседа для классификации
from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=3)
# fit - построение набора
clf.fit(X_train, y_train)
# predict - получаем прогнозы
print("Прогнозы на тестовом наборе: {}".format(clf.predict(X_test)))
# score - оценка обобщающей способности
print("Правильность на тестовом наборе: {:.2f}".format(clf.score(X_test, y_test)))
# визуализация границы принятия решений для 1,3,9 соседей, которая
# разбивает плоскость на 2 области: где алгоритм присваивает класс 0 и 1
fig, axes = plt.subplots(1, 3, figsize=(10, 3))
for n_neighbors, ax in zip([1, 3, 9], axes):
 clf = KNeighborsClassifier(n_neighbors=n_neighbors).fit(X, y)
 # поверхность
 mglearn.plots.plot_2d_separator(clf, X, fill=True, eps=0.5, ax=ax, alpha=.4)
 # точечки
 mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
 ax.set_title("количество соседей:{}".format(n_neighbors))
 ax.set_xlabel("признак 0")
 ax.set_ylabel("признак 1")
axes[0].legend(loc=3)
plt.show()

print("---------------------------")

# Загрузим набор данных о раке молочной железы и разобьем на обучающую и тестовую выборки
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
 cancer.data, cancer.target, stratify=cancer.target, random_state=66)
training_accuracy = []
test_accuracy = []
neighbors_settings = range(1, 11) # от 1 до 10 пробуем
# Оценка точности модели для разных значений количества соседей
for n_neighbors in neighbors_settings:
 clf = KNeighborsClassifier(n_neighbors=n_neighbors)
 clf.fit(X_train, y_train) # построение набора
 training_accuracy.append(clf.score(X_train, y_train))  # правильность на обучающем наборе
 test_accuracy.append(clf.score(X_test, y_test))  # правильность на тестовом наборе
plt.plot(neighbors_settings, training_accuracy, label="правильность на обучающем наборе")
plt.plot(neighbors_settings, test_accuracy, label="правильность на тестовом наборе")
plt.ylabel("Правильность")
plt.xlabel("количество соседей")
plt.legend()
plt.show()

print("---------------------------")

# Визуализация регрессии k ближайших соседей для различных значений соседей
# 3 точки тестового набора(зеленые *)
# прогноз использованием 1 соседа - целевое значение ближайшего соседа(синие *)
# если 3 соседа - прогноз это среднее значение соответствующих соседей
mglearn.plots.plot_knn_regression(n_neighbors=1)
plt.show()
mglearn.plots.plot_knn_regression(n_neighbors=3)
plt.show()

print("---------------------------")

# пример регрессии с использованием KNeighborsRegressor
from sklearn.neighbors import KNeighborsRegressor
X, y = mglearn.datasets.make_wave(n_samples=40)
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
reg = KNeighborsRegressor(n_neighbors=3)
reg.fit(X_train, y_train)  # построение набора
print("Прогнозы для тестового набора:\n{}".format(reg.predict(X_test)))  # прогнозы для тестового набора
print("R^2 на тестовом наборе: {:.2f}".format(reg.score(X_test, y_test)))  # правильность для тестового набора

fig, axes = plt.subplots(1, 3, figsize=(15, 4))
line = np.linspace(-3, 3, 1000).reshape(-1, 1)  # линия для прогнозов
for n_neighbors, ax in zip([1, 3, 9], axes):
    reg = KNeighborsRegressor(n_neighbors=n_neighbors)
    reg.fit(X_train, y_train)
    ax.plot(line, reg.predict(line))  # строим прогноз на основе линии
    ax.plot(X_train, y_train, '^', c=mglearn.cm2(0), markersize=8)  # обучающие данные
    ax.plot(X_test, y_test, 'v', c=mglearn.cm2(1), markersize=8)  # тестовые данные
    ax.set_title(
        "{} neighbor(s)\n train score: {:.2f} test score: {:.2f}".format(
            n_neighbors, reg.score(X_train, y_train), reg.score(X_test, y_test)))
    ax.set_xlabel("Признак")
    ax.set_ylabel("Целевая переменная")
axes[0].legend(["Прогнозы модели", "Обучающие данные/ответы",
                "Тестовые данные/ответы"], loc="best")
plt.show()