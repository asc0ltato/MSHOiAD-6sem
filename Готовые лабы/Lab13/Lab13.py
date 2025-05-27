import sklearn
import mglearn
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

# Линейная регрессия на простом наборе:
# kx+b(y^(прогноз, выдаваемый моделью) w[0]*x[0](признаки, наклон в мат) b)
# w[0] и b(сдвиг по Oy) - параметры модели, оцениваемые в ходе обучения
# это просто попытка найти прямую, которая макс хорошо описывает данные
mglearn.plots.plot_linear_regression_wave()
plt.show()

print("---------------------------")

from sklearn.linear_model import LinearRegression
X, y = mglearn.datasets.make_wave(n_samples=60)
from sklearn.model_selection import train_test_split # разделение на наборы
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)
lr = LinearRegression().fit(X_train, y_train) # обучение

# так как в wave используется 1 входной признак,
# lr.coef_ содержит только 1 элемент
# массив NumPy, в котором каждому элементу соответствует входной признак
print("lr.coef_: {}".format(lr.coef_)) # w - наклон, коэффициент
# всегда отдельное число с плавающей точкой
print("lr.intercept_: {}".format(lr.intercept_)) # b - сдвиг, константа
print("Правильность на обучающем наборе: {:.2f}".format(lr.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(lr.score(X_test, y_test)))
# результаты схожи, 0.66 указывает на недообучение (опасность невелика)

print("---------------------------")

# Линейная регрессия на более сложном наборе (506 примеров и 105 признаков)
X, y = mglearn.datasets.load_extended_boston()
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0)
lr = LinearRegression().fit(X_train, y_train)
# точно предсказываем на обучающем наборе, но на тестовом низкое значение
# это несоответствие является явным признаком переобучения
print("Правильность на обучающем наборе: {:.2f}".format(lr.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(lr.score(X_test, y_test)))

print("---------------------------")

# Гребневая регрессия:
# L2 регуляризация
# модель с более строгим ограничением, чем линейная, поэтому меньше
# вероятность переобучения. Позволяет найти компромисс между простой модели
# (w -> 0) и качеством ее работы на обучающем наборе. Компромисс задан alpa.
from sklearn.linear_model import Ridge
ridge = Ridge().fit(X_train, y_train) # обучение
print("Правильность на обучающем наборе: {:.2f}".format(ridge.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(ridge.score(X_test, y_test)))

# Чем выше alpha, тем меньше w (снижает качество работы модели на обучающем
# наборе, но улучшает ее обобщающую способность) (более жесткое ограничение
# на w, поэтому меньшие значения w для высокого alpha)
ridge10 = Ridge(alpha=10).fit(X_train, y_train)
print("Правильность на обучающем наборе: {:.2f}".format(ridge10.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(ridge10.score(X_test, y_test)))

# Сжимаем w в меньшей степени. При очень малых alpha, ограничение
# на коэффициенты не накладывается и получаем модель, напоминающую
# линейную регрессию (линейная без регуляризации)
ridge01 = Ridge(alpha=0.1).fit(X_train, y_train)
print("Правильность на обучающем наборе: {:.2f}".format(ridge01.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(ridge01.score(X_test, y_test)))

plt.plot(ridge.coef_, 's', label="Гребневая регрессия alpha=1")
plt.plot(ridge10.coef_, '^', label="Гребневая регрессия alpha=10")
plt.plot(ridge01.coef_, 'v', label="Гребневая регрессия alpha=0.1")
plt.plot(lr.coef_, 'o', label="Линейная регрессия")
plt.xlabel("Индекс коэффициента")
plt.ylabel("Оценка коэффициента")
# горизонтальная линия на 0 для сравнения
plt.hlines(0, 0, len(lr.coef_))
plt.ylim(-25, 25)
plt.legend()
plt.show()

# График зависимости точности гребневой регрессии от количества примеров
# графики, которые показывают качество работы модели в виде функции объема
# набора данных (кривые обучения)
# правильность на обучающем всегда выше правильности на тестовом в гребневой
# и линейной. На обучающем П гребневой ниже линейной. На тестовом у гребневой
# выше. При объеме менее 400 линейная не способна обучиться чему-либо.
# При достаточном объеме данных регуляризация становится менее важной и
# гребневая и линейная демонстрируют одинаковое качество работы
mglearn.plots.plot_ridge_n_samples()
plt.show()

print("---------------------------")

# Лассо:
# L1 регуляризация. Альтернатива гребневой. Некоторые w становятся равны 0.
# Некоторые признаки полностью исключаются из модели (авто отбор признаков).
# Это упрощает интерпретацию модели и может выявить более важные признаки
# При большом значении alpha модель просто их исключает, что может сделать ее проще и понятней.
# Лассо лучше всего работает, когда нужно избавиться от ненужных признаков.
from sklearn.linear_model import Lasso
lasso = Lasso().fit(X_train, y_train)
# Низкая П -> недообучение. Из 105 признаков только 4 используются
print("Правильность на обучающем наборе: {:.2f}".format(lasso.score(X_train, y_train)))
print("Правильность на контрольном наборе: {:.2f}".format(lasso.score(X_test, y_test)))
print("Количество использованных признаков: {}".format(np.sum(lasso.coef_ != 0)))

# Чтобы снизить недообучение, увеличиваем max_iter и уменьшаем alpha ->
# более сложная модель -> более высокая П, 33 признака
lasso001 = Lasso(alpha=0.01, max_iter=100000).fit(X_train, y_train)
print("Правильность на обучающем наборе: {:.2f}".format(lasso001.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(lasso001.score(X_test, y_test)))
print("Количество использованных признаков: {}".format(np.sum(lasso001.coef_ != 0)))

# Слишком низкое alpha -> нивелируем эффект регуляризации и получим
# переобучение (результат аналогичен линейной регрессии). 94 признака
lasso00001 = Lasso(alpha=0.0001, max_iter=100000).fit(X_train, y_train)
print("Правильность на обучающем наборе: {:.2f}".format(lasso00001.score(X_train, y_train)))
print("Правильность на тестовом наборе: {:.2f}".format(lasso00001.score(X_test, y_test)))
print("Количество использованных признаков: {}".format(np.sum(lasso00001.coef_ != 0)))

plt.plot(lasso.coef_, 's', label="Лассо alpha=1")
plt.plot(lasso001.coef_, '^', label="Лассо alpha=0.01")
plt.plot(lasso00001.coef_, 'v', label="Лассо alpha=0.0001")
plt.plot(ridge01.coef_, 'o', label="Гребневая регрессия alpha=0.1")
plt.legend(ncol=2, loc=(0, 1.05))
plt.ylim(-25, 25)
plt.xlabel("Индекс коэффициента")
plt.ylabel("Оценка коэффициента")
plt.show()