import sklearn
import mglearn
import matplotlib.pyplot as plt
import numpy as np

# сколько раз каждый признак появляется для каждого класса
X = np.array([[0, 1, 0, 1], [1, 0, 1, 1], [0, 0, 0, 1], [1, 0, 1, 0]])
y = np.array([0, 1, 0, 1])

counts = {}
for label in np.unique(y):
    counts[label] = X[y == label].sum(axis=0)

print("Частоты признаков:\n{}".format(counts))

print("-------------------------------------------------------------");
# как дерево ищет признаки
mglearn.plots.plot_animal_tree()
plt.show()

mglearn.plots.plot_tree_progressive()
plt.show()

print("-------------------------------------------------------------");
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

# обучаем дерево на cancer молочной железы
# сравниваем деревья с разной глубиной

cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, stratify=cancer.target, random_state=42)

tree = DecisionTreeClassifier(random_state=0)
tree.fit(X_train, y_train)

print("Правильность на тестовом наборе: {:.3f}".format(tree.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(tree.score(X_test, y_test)))

# тут срезаем лишнее, лучше для новых данных

tree = DecisionTreeClassifier(max_depth=4, random_state=0)
tree.fit(X_train, y_train)

print("Правильность на тестовом наборе: {:.3f}".format(tree.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(tree.score(X_test, y_test)))

print("-------------------------------------------------------------");
from sklearn.tree import export_graphviz

export_graphviz(tree, out_file="./Lab17/tree.dot",
                class_names=["malignant", "benign"],
                feature_names=cancer.feature_names,
                impurity=False, filled=True)

import graphviz

with open("./Lab17/tree.dot") as f:
    dot_graph = f.read()
graph = graphviz.Source(dot_graph)
graph.view()

print("-------------------------------------------------------------");
from sklearn import tree

# визуализация дерева и сохранение её в PDF
cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, stratify=cancer.target, random_state=42)
clf = DecisionTreeClassifier(max_depth=4, random_state=0)
clf.fit(X_train, y_train)

import pydotplus

dot_data = tree.export_graphviz(clf, out_file=None,
                           feature_names=cancer.feature_names,
                           class_names=cancer.target_names,
                           filled=True)

graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("./Lab17/cancer.pdf")

print("-------------------------------------------------------------");
# берем каждый признак из cancer и смотрим, как он влияет на дерево
from IPython.display import Image
dot_data = tree.export_graphviz(clf, out_file=None,
                                feature_names=cancer.feature_names,
                                class_names=cancer.target_names,
                                filled=True, rounded=True,
                                special_characters=True)
graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())

from sklearn.tree import DecisionTreeClassifier
tree = DecisionTreeClassifier().fit(X_train, y_train)
print("Важности признаков:\n{}".format(tree.feature_importances_))

def plot_feature_importances(model): # автоматически посчитанный вклад каждого признака
    n_features = cancer.data.shape[1]
    plt.barh(range(n_features), model.feature_importances_, align='center')
    plt.yticks(np.arange(n_features), cancer.feature_names)
    plt.xlabel("Важность признака")
    plt.ylabel("Признак")
    plt.tight_layout()
    plt.show()

plot_feature_importances(tree)

print("-------------------------------------------------------------");
# Feature importances: [0. 1.] -- важность признаков
tree = mglearn.plots.plot_tree_not_monotone()
plt.show()
# структура дерева решений
from IPython.display import display
display(tree)

print("-------------------------------------------------------------");
import pandas as pd

# как менялась цена оперативки по годам
# гибкое дерево, в отличие от регрессии

ram_prices = pd.read_csv("./Lab17/ram_price.csv")

plt.semilogy(ram_prices.date, ram_prices.price)
plt.xlabel("Год")
plt.ylabel("Цена $/Мбайт")
plt.show()

from sklearn.tree import DecisionTreeRegressor

data_train = ram_prices[ram_prices.date < 2000]
data_test = ram_prices[ram_prices.date >= 2000]
X_train = data_train.date.values.reshape(-1, 1)
y_train = np.log(data_train.price)

print("X:\n{}".format(X_train))
print("y:\n{}".format(y_train))

tree = DecisionTreeRegressor().fit(X_train, y_train)

from sklearn.linear_model import LinearRegression

linear_reg = LinearRegression().fit(X_train, y_train)

X_all = ram_prices.date.values.reshape(-1, 1)
pred_tree = tree.predict(X_all)
pred_lr = linear_reg.predict(X_all)

price_tree = np.exp(pred_tree)
price_lr = np.exp(pred_lr)

plt.semilogy(data_train.date, data_train.price, label="Обучающие данные")
plt.semilogy(data_test.date, data_test.price, label="Тестовые данные")
plt.semilogy(ram_prices.date, price_tree, label="Прогнозы дерева")
plt.semilogy(ram_prices.date, price_lr, label="Прогнозы линейной регрессии")
plt.legend()
plt.show()