import sklearn
import mglearn
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs, load_breast_cancer
from sklearn.svm import LinearSVC, SVC
from sklearn.model_selection import train_test_split
from mpl_toolkits.mplot3d import Axes3D

print("-------------------------------------------------------")
# синтетический набор данных
# классы линейно неразделимы
X, y = make_blobs(centers=4, random_state=8)
y = y % 2
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()

print("-------------------------------------------------------")
# классы линейно неразделимы с помощью прямой линии
# не может дать хорошее качество для этого набора данных
from sklearn.svm import LinearSVC
linear_svm = LinearSVC(dual='auto', max_iter=5000).fit(X, y)
mglearn.plots.plot_2d_separator(linear_svm, X)
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()

print("-------------------------------------------------------")
# трехмерное пространство и точка отображается с помощью трехмерной диаграммы рассеяния
# добавляем второй признак, возведенный в квадрат
# расширение за счет добавления третьего признака
X_new = np.hstack([X, X[:, 1:] ** 2])
from mpl_toolkits.mplot3d import Axes3D, axes3d
figure = plt.figure()
# визуализируем в 3D
ax = Axes3D(figure, elev=-152, azim=-26)
mask = y == 0
# сначала размещаем на графике все точки с y == 0, затем с y == 1 mask = y == 0
ax.scatter(X_new[mask, 0], X_new[mask, 1], X_new[mask, 2], color='b',s=60)
ax.scatter(X_new[~mask, 0], X_new[~mask, 1], X_new[~mask, 2], color='r', marker='^', s=60)
ax.set_xlabel("признак0")
ax.set_ylabel("признак1")
ax.set_zlabel("признак1 ** 2")
plt.show()

print("-------------------------------------------------------")
# можно разделить данные с помощью линий (линейной модели),
# но сперва нужно подогнать линейную модель к дополненным данным
linear_svm_3d = LinearSVC(dual='auto', max_iter=5000).fit(X_new, y)
coef, intercept = linear_svm_3d.coef_.ravel(), linear_svm_3d.intercept_

# показать границу принятия решений линейной модели
figure = plt.figure()
ax = Axes3D(figure, elev=-152, azim=-26)

xx = np.linspace(X_new[:, 0].min() - 2, X_new[:, 0].max() + 2, 50)
yy = np.linspace(X_new[:, 1].min() - 2, X_new[:, 1].max() + 2, 50)

XX, YY = np.meshgrid(xx, yy)
ZZ = (coef[0] * XX + coef[1] * YY + intercept) / -coef[2]
ax.plot_surface(XX, YY, ZZ, rstride=8, cstride=8, alpha=0.3)
ax.scatter(X_new[mask, 0], X_new[mask, 1], X_new[mask, 2], color='b', s=60)
ax.scatter(X_new[~mask, 0], X_new[~mask, 1], X_new[~mask, 2], color='r', marker='^', s=60)

ax.set_xlabel("признак0")
ax.set_ylabel("признак1")
ax.set_zlabel("признак1 ** 2")
plt.show()

print("-------------------------------------------------------")
# тут svm не линейная функция, а скорее эллипс
# красный - функция
ZZ = YY**2
dec = linear_svm_3d.decision_function(np.c_[XX.ravel(), YY.ravel(), ZZ.ravel()])
plt.contourf(XX, YY, dec.reshape(XX.shape), levels=[dec.min(), 0, dec.max()], cmap=mglearn.cm2, alpha=0.5)
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()

print("-------------------------------------------------------")
# Чтобы получить прогноз для новой точки, измеряется расстояние до каждого
# опорного вектора. Классификационное решение принимается, исходя из
# расстояний до опорных векторов, а также важности опорных векторов,
# полученных в процессе обучения (хранятся в атрибуте dual_coef_ класса SVC)

# обучаем машину опорных векторов на двумерном наборе данных
# граница принятия решений - черный
# опорные векторы - обведенные точки (лежат на границе между классами)
# гладкая нелинейная граница
from sklearn.svm import SVC
X, y = mglearn.tools.make_handcrafted_dataset()
svm = SVC(kernel='rbf', C=10, gamma=0.1).fit(X, y)
mglearn.plots.plot_2d_separator(svm, X, eps=.5)
mglearn.discrete_scatter(X[:, 0], X[:, 1], y)

# размещаем на графике опорные векторы sv = svm.support_vectors_
# метки классов опорных векторов определяются знаком дуальных коэффициентов
sv = svm.support_vectors_
sv_labels = svm.dual_coef_.ravel() > 0

mglearn.discrete_scatter(sv[:, 0], sv[:, 1], sv_labels, s=15, markeredgewidth=3)
plt.xlabel("Признак 0")
plt.ylabel("Признак 1")
plt.show()

print("-------------------------------------------------------")
# gamma - параметр формулы, который регулирует ширину ядра гаусса
# задает то, насколько близко будут расположены точки
# C - параметр регуляризации, ограничивает важность точки (ее dual_coef_)
# высокое гамма - сложная модель (небольшое = большой радиус ядра гаусса
# = многие точки расположенные по близости => гладкие границы)
# границы, которые большое фокусируются на отдельных точках, справа
# небольшое С = модель с жесткими ограничениями
fig, axes = plt.subplots(3, 3, figsize=(15, 10))
for ax, C in zip(axes, [-1, 0, 3]):
    for a, gamma in zip(ax, range(-1, 2)): mglearn.plots.plot_svm(log_C=C, log_gamma=gamma, ax=a)
axes[0, 0].legend(["class 0", "class 1", "sv class 0", "sv class 1"], ncol=4, loc=(.9, 1.2))
plt.show()

print("-------------------------------------------------------")
# svm с rbf-ядром к breast cancer (C=1, gamma= 1/n_features по умолчанию)
# svm чувствителен к параметрам и масштабированию данных
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, random_state=0)
svc = SVC()
svc.fit(X_train, y_train)
print("Правильность на обучающем наборе: {:.2f}".format(svc.score(X_train,
y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(svc.score(X_test, y_test)))
plt.show()

print("-------------------------------------------------------")
# min и max каждого признака в log-пространстве
# признаки имеют совершенно различные порядки величин
# для svm это проблема, для ядерного svm - разрушительные последствия
plt.plot(X_train.min(axis=0), 'o', label="min")
plt.plot(X_train.max(axis=0), '^', label="max")
plt.legend(loc=4)
plt.xlabel("Индекс признака")
plt.ylabel("Величина признака")
plt.yscale("log")
plt.show()

print("-------------------------------------------------------")
# решение проблемы - масштабирование всех признаков так, чтобы они имели
# примерно один и тот же масштаб (для ядерного, чтобы все признаки принимали
# значения от 0 до 1), сейчас сделаем вручную
# мин значение для каждого признака ОБУЧАЮЩЕГО
min_on_training = X_train.min(axis=0)
# ширина диапазона (max - min)
range_on_training = (X_train - min_on_training).max(axis=0)
# вычитаем минимальное значение и затем делим на ширину диапазона
# min=0 и max=1 для каждого признака
X_train_scaled = (X_train - min_on_training) / range_on_training
print("Минимальное значение для каждого признака\n{}".format(X_train_scaled.min(axis=0)))
print("Максимальное значение для каждого признака\n{}".format(X_train_scaled.max(axis=0)))

# ТО ЖЕ САМОЕ ДЛЯ ТЕСТОВОГО, используя min и ширину диапазона из обучающего
# признаки недообучения, когда качество модели на О и Т схоже, но далеко
# от 100%
X_test_scaled = (X_test - min_on_training) / range_on_training
svc = SVC()
svc.fit(X_train_scaled, y_train)
print("Правильность на обучающем наборе: {:.3f}".format( svc.score(X_train_scaled,y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(svc.score(X_test_scaled,y_test)))

# увеличим С, чтобы подогнать более сложную модель
svc = SVC(C=1000)
svc.fit(X_train_scaled, y_train)
print("Правильность на обучающем наборе: {:.3f}".format( svc.score(X_train_scaled,y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(svc.score(X_test_scaled,y_test)))