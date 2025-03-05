import sympy as sp
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as sco
import scipy.integrate as spi
from scipy.linalg import solve
from sklearn.linear_model import LinearRegression
import mglearn

#2.	Используя возможности SymPy:
#2.1.	Найдите производную функции f(x) = x2 + 1
x = sp.symbols('x')
f = x**2 + 1
df = sp.diff(f, x)
print("Производная f(x): ", df)

#2.2.	Найдите интеграл функции f(x) = x2 + 1 на отрезке [0, 1];
integral = sp.integrate(f, (x, 0, 1))
print("Интеграл f(x) на [0,1]: ", integral)

#2.3.	Найдите предел функции f(x) = 1/x2 + 1 при x→∞.
lim = sp.limit(1/x**2 + 1, x, sp.oo)
print("Предел f(x) при x→∞:", lim)

#3.	Используя возможности NumPy:
#3.1.	создайте одномерный массив из 20 целых случайных чисел;
array_1d = np.random.randint(0, 10, 20)
print("Одномерный массив:", array_1d)

#3.2.	преобразуйте созданный массив в двумерный массив размером [4,5];
array_2d = array_1d.reshape(4,5)
print("Двумерный массив:", array_2d)

#3.3.	разделите полученный массив на 2 массива;
array_split = np.split(array_2d, 2)
print("Разделенные массивы:", array_split)

#3.4.	найдите все заданные значения в первом массиве (например, равные 6);
found = np.where(array_split[0] == 6)
print("Индексы элементов со значением 6:", found)

#3.5.	подсчитайте количество найденных элементов;
count = np.count_nonzero(array_split[0] == 6)
print("Количество элементов со значением 6:", count)

#3.6.	во втором массиве найдите мин, макс и среднее;
min_val = np.min(array_split[1])
max_val = np.max(array_split[1])
mean_val = np.mean(array_split[1])
print(f"Минимальное: {min_val}, Максимальное: {max_val}, Среднее: {mean_val}")

#4.	Используя возможности Pandas:
#4.1.	Изучите структуры данных Series и Dataframe;
#4.2.	создайте объекты Series из массива NumPy, из словаря;
series_from_array = pd.Series(array_1d)
dict = {'a': 10, 'b': 20, 'c': 30}
series_from_dict = pd.Series(dict)
print("Series из массива:", series_from_array)
print("Series из словаря:", series_from_dict)

#4.3.	произведите с ним различные математические операции;
print("Series_from_array после **2:", series_from_array ** 2)
print("Series_from_array после +2:", series_from_array + 2)
print("Series_from_dict после -2:", series_from_dict - 2)
print("Series_from_dict после %:", series_from_dict % 2)

#4.4.	создайте объекты Dataframe из массива NumPy, словаря и объекта Series;
df_from_array = pd.DataFrame(array_2d, columns=['A', 'B', 'C', 'D', 'E'])
df_from_dict = pd.DataFrame(dict, index=['Value'])
df_from_series = pd.DataFrame({'Numbers': series_from_array})
print("DataFrame из массива:", df_from_array)
print("DataFrame из словаря:", df_from_dict)
print("DataFrame из Series:", df_from_series)

#5.	Продемонстрируйте работу с пакетом Matplotlib:
#5.1.	Постройте график функции f(x) = x2 + 1;
x = np.linspace(-20,20, 400) # Массив
y = x**2 + 1
plt.plot(x,y, label = 'f(x) = x2 + 1') # Рисуем
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.title('График функции f(x)')
plt.grid()
plt.show()

#5.2.	Постройте график поверхности функции f(x, y) = x2 + 2y2 + 1;
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') # Трехмерная область
X = np.linspace(-5,5, 200)
Y = np.linspace(-5,5, 200)
X, Y = np.meshgrid(X, Y) # Координатная сетка
Z = X**2 + 2*Y**2 + 1
ax.plot_surface(X, Y, Z) # Строит график
plt.title('График поверхности f(x, y)')
plt.show()

#5.3.	Постройте несколько видов диаграмм;
# Гистограмма
data = np.random.randint(0, 100, 1000)
plt.figure()
plt.hist(data, bins=20, color='pink', edgecolor='black', alpha=0.7)
plt.xlabel('Значения')
plt.ylabel('Частота')
plt.title('Гистограмма случайных чисел')
plt.show()

# Круговая диаграмма
labels = ['Спать', 'Есть', 'Смотреть аниме', 'Учиться']
data = [50, 20, 20, 10]
plt.figure()
plt.pie(data, labels=labels, autopct='%1.1f%%')
plt.title('Круговая диаграмма')
plt.show()

# Столбчатая диаграмма
plt.figure()
plt.bar(labels, data, color='pink', edgecolor='black', alpha=0.7)
plt.title('Столбчатая диаграмма')
plt.show()

#6.	Установите следующие пакеты и ознакомьтесь, для чего они предназначены:
#6.1.	Scipy
def f(x):
    return x**2 - 4
root = sco.fsolve(f, x0=1)
print("Корень уравнения:", root[0])

def f(x):
    return x**2
integral, error = spi.quad(f, 0, 2)
print("Значение интеграла:", integral)

A = np.array([[2, 1], [1, 3]])  # Коэффициенты
b = np.array([1, 4])  # Правая часть
solution = solve(A, b)
print("Решение системы:" , solution)

#6.2.	IPython
#lsmagic
#%time
#history
#??sum

#6.3.	Sklearn
X = np.array([[1], [2], [3], [4], [5]])
y = np.array([2, 4, 6, 8, 10])
model = LinearRegression()
model.fit(X, y)
print("Найденный коэффициент (w):", model.coef_[0])
print("Найденное смещение (b):", model.intercept_)
print("Предсказанное значение y для x = 6: ", model.predict([[6]]))

#6.4.	Mglearn
plt.figure()
plt.scatter(X, y, color='blue', label='Исходные данные')
plt.plot(X, model.predict(X), color='red', label='Линейная регрессия')
plt.scatter([6], model.predict([[6]]), color='pink', label='Предсказание x=6')
plt.xlabel("X (признак)")
plt.ylabel("y (целевая переменная)")
plt.legend()
plt.title("Линейная регрессия: y = 2x")
plt.grid()
plt.show()