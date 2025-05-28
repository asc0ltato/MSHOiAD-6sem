import mglearn
import sklearn
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_digits
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

print('--------------------------------')
# Визуализация иллюстрации работы NMF
mglearn.plots.plot_nmf_illustration()
plt.show()
print('--------------------------------')
# На этом графике показано, как NMF раскладывает данные на компоненты,
# которые неотрицательны. Это отличие от PCA, где компоненты могут быть отрицательными.
# NMF ищет положительные компоненты, что делает интерпретацию более естественной.

from sklearn.decomposition import NMF, PCA

digits = load_digits()
X_train, X_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.2, random_state=42)

nmf = NMF(n_components=15, random_state=0)
nmf.fit(X_train)
X_train_nmf = nmf.transform(X_train)
X_test_nmf = nmf.transform(X_test)

# Визуализация компонентов NMF для изображений цифр
fix, axes = plt.subplots(3, 5, figsize=(15, 12), subplot_kw={'xticks': (), 'yticks': ()})
image_shape = (8, 8)
for i, (component, ax) in enumerate(zip(nmf.components_, axes.ravel())):
    ax.imshow(component.reshape(image_shape))
    ax.set_title("{}. component".format(i))
plt.show()
print('--------------------------------')
# Здесь показаны 15 компонент, которые NMF извлек из данных.
# Каждая компонента - это "часть" образа цифры, например, отдельные элементы лиц или цифр.

compn = 3
# Сортируем обучающую выборку по значению 3-й компоненты в убывающем порядке
inds = np.argsort(X_train_nmf[:, compn])[::-1]
fig, axes = plt.subplots(2, 5, figsize=(15, 8), subplot_kw={'xticks': (), 'yticks': ()})
for i, (ind, ax) in enumerate(zip(inds, axes.ravel())):
    ax.imshow(X_train[ind].reshape(image_shape))
plt.show()
print('--------------------------------')
# Здесь мы выводим первые 10 изображений с наибольшими значениями по 3-й компоненте.

compn = 7
# Аналогично для 7-й компоненты
inds = np.argsort(X_train_nmf[:, compn])[::-1]
fig, axes = plt.subplots(2, 5, figsize=(15, 8),
                        subplot_kw={'xticks': (), 'yticks': ()})
for i, (ind, ax) in enumerate(zip(inds, axes.ravel())):
    ax.imshow(X_train[ind].reshape(image_shape))
plt.show()
print('--------------------------------')
# Аналогично, показываем изображения, наиболее соответствующие 7-й компоненте.
# Это помогает визуализировать, какие черты цифр эта компонента выделяет.

# Работа с синтетическими сигналами
S = mglearn.datasets.make_signals()
plt.figure(figsize=(6, 1))
plt.plot(S, '-')
plt.xlabel("Время")
plt.ylabel("Сигнал")
plt.show()
print('--------------------------------')
# Три исходных синтетических сигнала, которые будем пытаться восстановить.

# Создаем смешанные наблюдения на основе этих сигналов
A = np.random.RandomState(0).uniform(size=(100, 3))
X = np.dot(S, A.T)
print("Форма измерений: {}".format(X.shape))
print('--------------------------------')
# Форма измерений (2000, 3) означает, что у нас 2000 наблюдений с 3 измерениями.
# Исходные сигналы перемешаны.

nmf = NMF(n_components=3, random_state=42)
S_ = nmf.fit_transform(X)
print("Форма восстановленного сигнала: {}".format(S_.shape))
print('--------------------------------')
# Восстановленные с помощью NMF сигналы имеют такую же форму, как исходные (2000, 3).
# Это значит, что NMF успешно выделил 3 компоненты, пытаясь "разложить" смешанные данные.

pca = PCA(n_components=3)
H = pca.fit_transform(X)

models = [X, S, S_, H]
names = ['Наблюдения (первые три измерения)', 'Фактические источники',
         'Сигналы, восстановленные NMF', 'Сигналы, восстановленные PCA']
fig, axes = plt.subplots(4, figsize=(8, 4), gridspec_kw={'hspace': .5},
                         subplot_kw={'xticks': (), 'yticks': ()})
for model, name, ax in zip(models, names, axes):
    ax.set_title(name)
    ax.plot(model[:, :3], '-')
plt.show()
print('--------------------------------')
# На графиках показано сравнение:
# - исходные смешанные наблюдения,
# - истинные (фактические) исходные сигналы,
# - сигналы, восстановленные NMF,
# - сигналы, восстановленные PCA.
# Видно, что NMF лучше восстанавливает исходные сигналы, так как учитывает неотрицательность.
# PCA "размазывает" сигналы, пытаясь объяснить максимальную дисперсию.

# Визуализация образцов из набора digits
digits = load_digits()
fig, axes = plt.subplots(2, 5, figsize=(10, 5), subplot_kw={'xticks': (), 'yticks': ()})
for ax, img in zip(axes.ravel(), digits.images):
    ax.imshow(img)
plt.show()
print('--------------------------------')
# Примеры изображений рукописных цифр из набора данных.

# Визуализация результатов PCA для digits (две главные компоненты)
pca = PCA(n_components=2)
pca.fit(digits.data)
digits_pca = pca.transform(digits.data)
colors = ["#476A2A", "#7851B8", "#BD3430", "#4A2D4E", "#875525", "#A83683",
          "#4E655E", "#853541", "#3A3120", "#535D8E"]
plt.figure(figsize=(10, 10))
plt.xlim(digits_pca[:, 0].min(), digits_pca[:, 0].max())
plt.ylim(digits_pca[:, 1].min(), digits_pca[:, 1].max())
for i in range(len(digits.data)):
    plt.text(digits_pca[i, 0], digits_pca[i, 1],
             str(digits.target[i]),
             color=colors[digits.target[i]],
             fontdict={'weight': 'bold', 'size': 9})
plt.xlabel("Первая главная компонента")
plt.ylabel("Вторая главная компонента")
plt.show()
print('--------------------------------')
# График отображает рукописные цифры, спроецированные на первые две главные компоненты.
# Каждая цифра представлена своим символом, раскрашенным по классу.
# Видно, что некоторые классы отделяются неплохо (например, 0, 6, 4), но большинство пересекаются.

# Визуализация методом t-SNE
from sklearn.manifold import TSNE
tsne = TSNE(random_state=42)
digits_tsne = tsne.fit_transform(digits.data)

plt.figure(figsize=(10, 10))
plt.xlim(digits_tsne[:, 0].min(), digits_tsne[:, 0].max() + 1)
plt.ylim(digits_tsne[:, 1].min(), digits_tsne[:, 1].max() + 1)
for i in range(len(digits.data)):
    plt.text(digits_tsne[i, 0], digits_tsne[i, 1],
             str(digits.target[i]),
             color=colors[digits.target[i]],
             fontdict={'weight': 'bold', 'size': 9})
plt.xlabel("t-SNE признак 0")
plt.xlabel("t-SNE признак 1")
plt.show()
print('--------------------------------')
# На графике t-SNE видно, что алгоритм лучше отделяет классы по сравнению с PCA.
# t-SNE пытается сохранить локальные расстояния между точками,
# поэтому данные того же класса группируются плотнее, хотя метод не использует метки классов.
# Это хорошо показывает возможности нелинейного снижения размерности для визуализации.