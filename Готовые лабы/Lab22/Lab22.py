import mglearn
import sklearn
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore', category=UserWarning)

# Машинное обучение без учителя.
# Включает все виды машинного обучения, когда ответ неизвестен и отстуствует
# учитель, указывающий ответ алгоритму. Есть только входные данные и
# алгоритму необходимо извлечь знания из этих данных
# 2 вида: Преобразование данных (новое представление, обработать легче, чем
# исходное, из высокоразмерного представления из множества признаков обобщая
# хар-ки получаем меньшее кол-во признаков, получение двумерного пространства)
# (поиск компонент, из которых состоят данные (выделение тем из ворда)) и
# Кластеризация - разбитие данных на группы схожих между собой элементов.
# (извлечение лиц и разделить их на группы лиц на фотках)

# Проблема - оценка полезности инфы. Эти алгоритмы применяются к данным,
# которые не содержат никаких меток -> не знаем, какой должен быть
# правильный ответ -> сложно судить о качестве работы модели
# Единственный способ оценить результат - ручная проверка результата

# Используются в разведочных целях, когда чел хочет лучше изучить сами данные
# служат этапом предварительной обработки данных для алгоритмов МО с учителем

print("-------------------------------------------------------")
# Различные способы масштабирования и предварительной обработки данных
# Синтетический 2 классовый набор данных с 2 признаками
# StandardScaler - для каждого признака среднее 0, дисперсия 1 -> признаки
# имеют один и тот же масштаб
# RobustScaler аналогичен в плане масштаба, но вместо среднего и дисперсии
# использует медиану и квартили -> игнорирует точки данных, которые сильно
# отличаются от остальных (ошибки измерений, например (выбросы))
# MinMaxScaler сдвигает данные, что все признаки находились [0,1]
# Normalizer - иной вид масштабирования. Масштабирует каждую точку так, чтобы
# вектор признаков имел евклидову длину 1. Проецирует точку данных на окружность
# с R=1. Вектор умножается на инверсию своей длины. Используется, когда
# важным является направление, но не длина вектора признаков
"In[2]:"
mglearn.plots.plot_scaling()
plt.show()

print("-------------------------------------------------------")
# набор из 569 точек 30 признаков (426 в обучающем и 143 в тестовом)
"In[3]:"
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, random_state=1)
print(X_train.shape)
print(X_test.shape)

"In[4]:"
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

# Подгоняем scaler на обучающих. Для MinMaxScaler fit вычисляет min и max
# значения каждого признака на обучающем
# В отличие от классификаторов и регрессоров при вызове метода fit scaler
# работает с данными (X_train), а ответы (y_train) не используются
"In[5]:"
scaler.fit(X_train)

# Чтобы применить преобразование, т.е. отмасштабировать (scale) обучающие,
# метод transform - модель возвращает новые данные
# Преобразованные данные имеют такую же форму, что и исходные данные – признаки
# просто смещены и масштабированы. Диапазон теперь [0,1]
"In[6]:"
min_on_training = X_train.min(axis=0)
range_on_training = (X_train - min_on_training).max(axis=0)
X_train_scaled = (X_train - min_on_training) / range_on_training
print("форма преобразованного массива: {}".format(X_train_scaled.shape))
print("min значение признака до масштабирования:\n {}".format(X_train.min(axis=0)))
print("max значение признака до масштабирования:\n {}".format(X_train.max(axis=0)))
print("min значение признака после масштабирования:\n {}".format( X_train_scaled.min(axis=0)))
print("max значение признака после масштабирования:\n {}".format( X_train_scaled.max(axis=0)))

# Чтобы применить SVM к масштабированным данным, должны преобразовать и
# тестовый набор -> transform для X_text
# Не в [0,1], тк все типы масштабирования всегда применяют одинаковое преобразование
# к обуч и тестовому. Значит, что transform всегда вычитает min из обучающего
# и делит на ширину диапазона, вычисленную для обучающего. Min и ширина диапазона
# для обучающего могут отличаться от min и ширины диапазона для тестового
"In[7]:"
X_test_scaled = (X_test - min_on_training) / range_on_training
print("min значение признака после масштабирования:\n{}".format(X_test_scaled.min(axis=0)))
print("max значение признака после масштабирования:\n{}".format(X_test_scaled.max(axis=0)))

print("-------------------------------------------------------")
# Чтобы модель контролируемого обучения работала на тестовом наборе, важно
# преобразовать обучающий и тестовый наборы одинаковым образом.
# Пример показывает, что произошло бы, если бы мы использовали минимальное
# значение и ширину диапазона, отдельно вычисленные для тестового набора:
"In[8]:"
from sklearn.datasets import make_blobs
X, _ = make_blobs(n_samples=50, centers=5, random_state=4, cluster_std=2)
X_train, X_test = train_test_split(X, random_state=5, test_size=.1)
fig, axes = plt.subplots(1, 3, figsize=(13, 4))
axes[0].scatter(X_train[:, 0], X_train[:, 1],
c=mglearn.cm2(0), label="Обучающий набор", s=60)
axes[0].scatter(X_test[:, 0], X_test[:, 1], marker='^',
c=mglearn.cm2(1), label="Тестовый набор", s=60)
axes[0].legend(loc='upper left')
axes[0].set_title("Исходные данные")

scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)

axes[1].scatter(X_train_scaled[:, 0], X_train_scaled[:, 1],
c=mglearn.cm2(0), label="Обучающий набор", s=60)

axes[1].scatter(X_test_scaled[:, 0], X_test_scaled[:, 1], marker='^', c=mglearn.cm2(1), label="Тестовый набор", s=60)
axes[1].set_title("Масштабированные данные")

test_scaler = MinMaxScaler()
test_scaler.fit(X_test)
X_test_scaled_badly = test_scaler.transform(X_test)

axes[2].scatter(X_train_scaled[:, 0], X_train_scaled[:, 1],
c=mglearn.cm2(0), label="Обучающий набор", s=60)

axes[2].scatter(X_test_scaled_badly[:, 0], X_test_scaled_badly[:, 1], marker='^', c=mglearn.cm2(1), label="Тестовый набор", s=60)
axes[2].set_title("Неправильно масштабированные данные")
for ax in axes:
    ax.set_xlabel("Признак 0")
    ax.set_ylabel("Признак 1")
plt.show()

# 1 график - не масштабированный
# 2 график - масштабированы с помощью MinMaxScaler. Метод для обучающего,
# метод transform для обучающего и тестового
# Наборы на 1 и 2 идентичны, изменились метки осей (на втором от 0 до 1 признаки)
# Min и max значения признаков в тестовом не равны 0 и 1
# 3 - что произойдет, если отмасштабируем обучающий и тестовый наборы отдельно
# Min и max в обучающем и тестовом равны 0 и 1
print("-------------------------------------------------------")
# Преобразование обучающего fit_transform - эффективно
"In[9]:"
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_scaled = scaler.fit(X).transform(X)
X_scaled_d = scaler.fit_transform(X)

print("-------------------------------------------------------")
# Правильность на тестовом 0.63 (без масштабирования)
"In[10]:"
from sklearn.svm import SVC
X_train, X_test, y_train, y_test = train_test_split(cancer.data, cancer.target, random_state=0)
svm = SVC(C=100)
svm.fit(X_train, y_train)
print("Правильность на тестовом наборе: {:.2f}".format(svm.score(X_test, y_test)))

# Отмасштабируем данные с помощью MinMaxScaler перед тем, как подгонять SVC (0.97)
"In[11]:"
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
svm.fit(X_train_scaled, y_train)
print("Правильность на масштабированном тестовом наборе: {:.2f}".format( svm.score(X_test_scaled, y_test)))

print("-------------------------------------------------------")
# Легкая смена алгоритма MinMaxScaler на StandardScaler (0.96)
"In[12]:"
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
svm.fit(X_train_scaled, y_train)
print("Правильность SVM на тестовом наборе: {:.2f}".format(svm.score(X_test_scaled, y_test)))