import mglearn
import matplotlib.pyplot as plt
import numpy as np
import graphviz
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from IPython.display import display
print("-------------------------------------------------------")
# графики функций активации (с одним скрытым слоем)
# входные признаки и прогнозы в виде узлов, коэффициенты
# - в виде соединений между узлами, выход - сумма входов
# вычисление скрытых элементов (промежуточный этап обработки)
# многослойный персептрон с одним скрытым слоем
display(mglearn.plots.plot_single_hidden_layer_graph())
# сравнение двух функций активации: tanh и ReLU
# гиперболический тангенс - сглаженная S-образная
# relu - обрезает отрицательные значения
line = np.linspace(-3, 3, 100)
plt.plot(line, np.tanh(line), label="tanh")
plt.plot(line, np.maximum(line, 0), label="relu")
plt.legend(loc="best")
plt.xlabel("x")
plt.ylabel("relu(x), tanh(x)")
plt.show()

print("-------------------------------------------------------")
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_moons
# на данных make_moons
X, y = make_moons(n_samples=100, noise=0.25, random_state=3)
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=42)

# MLPClassifier — многослойный персептрон. solver='lbfgs' — метод оптимизации.
# логистическая регрессия
mlp = MLPClassifier(solver='lbfgs', max_iter=1000, random_state=0).fit(X_train, y_train)
mglearn.plots.plot_2d_separator(mlp, X_train, fill=True, alpha=0.3)
mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()

print("-------------------------------------------------------")
# Модель с одним скрытым слоем из 10 нейронов
mlp = MLPClassifier(solver='lbfgs', max_iter=1000, random_state=0, hidden_layer_sizes=[10])
mlp.fit(X_train, y_train)
mglearn.plots.plot_2d_separator(mlp, X_train, fill=True, alpha=0.3)
mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()

print("-------------------------------------------------------")
# Модель с двумя скрытыми слоями по 10 нейронов
# более глубокая сеть, сложная зависимость
mlp = MLPClassifier(solver='lbfgs', max_iter=1000, random_state=0, hidden_layer_sizes=[10, 10])
mlp.fit(X_train, y_train)
mglearn.plots.plot_2d_separator(mlp, X_train, fill=True, alpha=0.3)
mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()

print("-------------------------------------------------------")
# Модель с активацией tanh (к задачам, где нужны и отриц и полож значения)
mlp = MLPClassifier(solver='lbfgs', max_iter=1000, activation='tanh', random_state=0, hidden_layer_sizes=[10, 10])
mlp.fit(X_train, y_train)
mglearn.plots.plot_2d_separator(mlp, X_train, fill=True, alpha=0.3)
mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()

print("-------------------------------------------------------")
# Влияние параметров альфа модели (коэффициент L2-регуляризации).
# Чем больше, тем сильнее штраф за большие веса.
# Помогает избежать переобучения
fig, axes = plt.subplots(2, 4, figsize=(20, 8))

for axx, n_hidden_nodes in zip(axes, [10, 100]):
    for ax, alpha in zip(axx, [0.0001, 0.01, 0.1, 1]):
        mlp = MLPClassifier(solver='lbfgs', random_state=0, hidden_layer_sizes=[n_hidden_nodes, n_hidden_nodes], alpha=alpha)
        mlp.fit(X_train, y_train)
        mglearn.plots.plot_2d_separator(mlp, X_train, fill=True, alpha=0.3, ax=ax)
        mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train, ax=ax)
        ax.set_title(f"n_hidden=[{n_hidden_nodes}, {n_hidden_nodes}]\nalpha={alpha:.4f}")

plt.show()

print("-------------------------------------------------------")
# Влияние random_state
# Разные инициализации весов могут сильно менять поведение модели
fig, axes = plt.subplots(2, 4, figsize=(20, 8))

for i, ax in enumerate(axes.ravel()):
    mlp = MLPClassifier(solver='lbfgs', max_iter=1000, random_state=i, hidden_layer_sizes=[100, 100])
    mlp.fit(X_train, y_train)
    mglearn.plots.plot_2d_separator(mlp, X_train, fill=True, alpha=0.3, ax=ax)
    mglearn.discrete_scatter(X_train[:, 0], X_train[:, 1], y_train, ax=ax)

plt.show()

print("-------------------------------------------------------")
from sklearn.datasets import load_breast_cancer
# опять рак
cancer = load_breast_cancer()
print("Максимальные значения характеристик:\n{}".format(cancer.data.max(axis=0)))

X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, random_state=0)
# Без масштабирования
# Без приведения признаков к единому масштабу сеть обучается плохо.
# Признаки могут перекрывать друг друга
mlp = MLPClassifier(random_state=42, max_iter=1000)
mlp.fit(X_train, y_train)
print("Правильность на обучающем наборе: {:.2f}".format(mlp.score(X_train, y_train)))
print("Правильности на тестовом наборе: {:.2f}".format(mlp.score(X_test, y_test)))

# Масштабирование данных (нормализация)
# Важно для нейросетей. Ускоряет обучение
min_on_training = X_train.min(axis=0)
range_on_training = (X_train - min_on_training).max(axis=0)
X_train_scaled = (X_train - min_on_training) / range_on_training
mean_on_train = X_train.mean(axis=0)
std_on_train = X_train.std(axis=0)
X_test_scaled = (X_test - mean_on_train) / std_on_train

# С увеличением количества итераций
mlp = MLPClassifier(max_iter=1000, random_state=0)
mlp.fit(X_train_scaled, y_train)
print("Правильность на обучающем наборе: {:.3f}".format(mlp.score(X_train_scaled, y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(mlp.score(X_test_scaled, y_test)))

# Регуляризация alpha=1
mlp = MLPClassifier(max_iter=1000, alpha=1, random_state=0)
mlp.fit(X_train_scaled, y_train)
print("Правильность на обучающем наборе: {:.3f}".format(mlp.score(X_train_scaled, y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(mlp.score(X_test_scaled, y_test)))

# Визуализация весов (между входными признаками и первым скрытым слоем)
# Важность признаков оценивается как ярче/темнее -> сильное влияние
plt.figure(figsize=(20, 5))
plt.imshow(mlp.coefs_[0], interpolation='none', cmap='viridis')
plt.yticks(range(30), cancer.feature_names)
plt.xlabel("Столбцы матрицы весов")
plt.ylabel("Входная характеристика")
plt.colorbar()
plt.show()