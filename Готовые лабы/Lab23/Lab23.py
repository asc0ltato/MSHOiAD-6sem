import mglearn
import sklearn
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

# PCA — метод, поворачивающий пространство признаков так, чтобы максимизировать
# дисперсию по новым осям (главным компонентам). Первая компонента несет
# максимум информации, вторая — максимум информации при ортогональности
# к первой

print('-----------------------------')
# PCA на синтетических данных
# PCA поворачивает данные так, чтобы первая главная компонента была
# направлена в сторону максимальной дисперсии данных, а вторая — ортогональна первой
mglearn.plots.plot_pca_illustration()
plt.show()

print('-----------------------------')
# Гистограммы распределения значений признаков для двух классов (доброкачественные и злокачественные опухоли)
# Цвета показывают различия между классами, что помогает визуально оценить информативность признаков.
# Признаки с сильным перекрытием гистограмм (smoothness error) малоинформативны,
# а те, где гистограммы мало перекрываются (worst concave points), хорошо разделяют классы.
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
fig, axes = plt.subplots(15, 2, figsize=(10, 20))
malignant = cancer.data[cancer.target == 0]
benign = cancer.data[cancer.target == 1]
ax = axes.ravel()
for i in range(30):
    _, bins = np.histogram(cancer.data[:, i], bins=50)
    ax[i].hist(malignant[:, i], bins=bins, color=mglearn.cm3(0), alpha=.5)
    ax[i].hist(benign[:, i], bins=bins, color=mglearn.cm3(2), alpha=.5)
    ax[i].set_title(cancer.feature_names[i])
    ax[i].set_yticks(())
    ax[0].set_xlabel("Значение признака")
    ax[0].set_ylabel("Частота")
    ax[0].legend(["доброкачественная", "злокачественная"], loc="best")
fig.tight_layout()
plt.show()

print('-----------------------------')
# Масштабируем данные, чтобы признаки имели среднее 0 и дисперсию 1.
# Это важно для PCA, т.к. признаки с большим масштабом могут доминировать при поиске главных компонент
from sklearn.datasets import load_breast_cancer
cancer = load_breast_cancer()
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(cancer.data)
X_scaled = scaler.transform(cancer.data)

from sklearn.decomposition import PCA
# Создаем объект PCA, оставляем только 2 главные компоненты для визуализации
pca = PCA(n_components=2)
# Подгоняем модель PCA на наборе данных breast cancer
pca.fit(X_scaled)
# Преобразуем данные к первым двум главным компонентам
X_pca = pca.transform(X_scaled)
print("Форма исходного массива: {}".format(str(X_scaled.shape)))  # (569, 30) - 569 объектов, 30 признаков
print("Форма массива после сокращения размерности: {}".format(str(X_pca.shape)))  # (569, 2) - уменьшение размерности до 2
# Строим график первых двух главных компонент, классы выделены цветом
# Классы отображены разными цветами — видно, что PCA хорошо разделяет два класса
plt.figure(figsize=(8, 8))
mglearn.discrete_scatter(X_pca[:, 0], X_pca[:, 1], cancer.target)
plt.legend(cancer.target_names, loc="best")
plt.gca().set_aspect("equal")
plt.xlabel("Первая главная компонента")
plt.ylabel("Вторая главная компонента")
plt.show()

print('-----------------------------')
# Каждая компонента — это набор весов для исходных признаков, показывающих их вклад.
print("форма главных компонент: {}".format(pca.components_.shape))  # (2, 30) — 2 компоненты, 30 признаков
print("компоненты PCA:\n{}".format(pca.components_))  # Веса каждого признака в главных компонентах

# Тепловая карта коэффициентов признаков в главных компонентах.
# Это помогает понять, какие признаки сильнее влияют на каждую компоненту.
# В первой компоненте веса однородны по знаку, что означает общую корреляцию признаков.
# Во второй — веса имеют разный знак, показывая более сложные взаимодействия.
plt.matshow(pca.components_, cmap='viridis')
plt.yticks([0, 1], ["Первая компонента", "Вторая компонента"])
plt.colorbar()
plt.xticks(range(len(cancer.feature_names)), cancer.feature_names, rotation=60, ha='left')
plt.xlabel("Характеристика")
plt.ylabel("Главные компоненты")
plt.show()

print('-----------------------------')
# Работа с набором лиц LFW (Labeled Faces in the Wild)
# conda install -c anaconda openssl
from sklearn.datasets import fetch_lfw_people
# Загружаем фотографии людей, у которых не менее 20 лиц на фото, уменьшаем размер для ускорения обработки
people = fetch_lfw_people(min_faces_per_person=20, resize=0.7)
image_shape = people.images[0].shape
# Визуализируем несколько изображений с подписями имен
fix, axes = plt.subplots(2, 5, figsize=(15, 8), subplot_kw={'xticks': (), 'yticks': ()})
for target, image, ax in zip(people.target, people.images, axes.ravel()):
 ax.imshow(image)
 ax.set_title(people.target_names[target])
plt.show()
print("форма массива изображений лиц: {}".format(people.images.shape))  # (3023, 87, 65)
print("количество классов: {}".format(len(people.target_names)))  # 62 класса (человека)

print('-----------------------------')
# Анализ частоты изображений на каждого человека - видно, что некоторых людей (Джордж Буш 530)
# много, что приводит к дисбалансу классов.
# Вычисляем частоту встречаемости каждого ответа
counts = np.bincount(people.target)
# Печатаем частоты рядом с ответами
for i, (count, name) in enumerate(zip(counts, people.target_names)):
 print("{0:25} {1:3}".format(name, count), end=' ')
 if (i + 1) % 3 == 0: print()
 # Для балансировки ограничиваем число изображений каждого человека до 50
mask = np.zeros(people.target.shape, dtype=np.bool_)
for target in np.unique(people.target):
 mask[np.where(people.target == target)[0][:50]] = 1
X_people = people.data[mask]
y_people = people.target[mask]
# Для получения большей стабильности масштабируем шкалу оттенков серого так, чтобы значения
# были в диапазоне от 0 до 1 вместо использования шкалы значений от 0 до 255.
X_people = X_people / 255.
from sklearn.neighbors import KNeighborsClassifier

# Разбиваем данные на обучающий и тестовый наборы
X_train, X_test, y_train, y_test = train_test_split(
 X_people, y_people, stratify=y_people, random_state=0)
# Обучаем классификатор ближайшего соседа с k=1
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train, y_train)
print("Правильность на тестовом наборе для 1-nn: {:.2f}".format(knn.score(X_test, y_test))) # 0.22

print('-----------------------------')
# PCA с операцией выбеливания (whitening),
# которая нормализует дисперсию по всем главным компонентам, улучшая работу классификатора
mglearn.plots.plot_pca_whitening()
plt.show()

print('-----------------------------')
# Применяем PCA с 100 компонентами и whitening для снижения размерности изображений
pca = PCA(n_components=100, whiten=True, random_state=0).fit(X_train)
X_train_pca = pca.transform(X_train)
X_test_pca = pca.transform(X_test)
print("обучающие данные после PCA: {}".format(X_train_pca.shape))  # (train_size, 100)

print('-----------------------------')
# Обучаем классификатор KNN на новых признаках после PCA.
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train_pca, y_train)
# 0.3 - заметное улучшение, т.к. PCA помогает выделить наиболее значимые признаки
print("Правильность на тестовом наборе: {:.2f}".format(knn.score(X_test_pca, y_test)))
# (100, 5655) - 100 главных компонент, каждая длиной как исходное изображение
print("форма pca.components_: {}".format(pca.components_.shape))

print('-----------------------------')
# Визуализируем главные компоненты в виде изображений («eigenfaces»),
# показывая, какие шаблоны "изучает" PCA (распределение освещенности, контраст)
mglearn.plots.plot_pca_faces(X_train, X_test, image_shape)
plt.show()

print('-----------------------------')
# Диаграмма рассеяния обучающих данных по первым двум главным компонентам.
# Видим сильное перекрытие классов — простое двумерное пространство недостаточно для точной классификации лиц.
mglearn.discrete_scatter(X_train_pca[:, 0], X_train_pca[:, 1], y_train)
plt.xlabel("Первая главная компонента")
plt.ylabel("Вторая главная компонента")
plt.show()