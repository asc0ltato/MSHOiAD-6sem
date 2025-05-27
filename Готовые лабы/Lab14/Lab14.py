import mglearn
import sklearn
import matplotlib.pyplot as plt

print("---------------------------")

# Границы принятия решений линейного SVM и логистической регрессии для forge
# Обе модели имеют схожие границы принятия решений (net) и неправильно
# классифицировали 2 точки. По умолчанию L2 регуляризация (гребневая)
# С - компромиссный параметр (определяет степень регуляризации), чем выше С,
# тем меньшая регуляризация (алгоритмы пытаются подогнать модель к обучающим
# как можно лучше, важно, чтобы каждая точка была классифицирована отдельно)
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
X, y = mglearn.datasets.make_forge()
fig, axes = plt.subplots(1, 2, figsize=(10, 3))
for model, ax in zip([LinearSVC(), LogisticRegression()], axes):
    clf = model.fit(X, y)
    mglearn.plots.plot_2d_separator(clf, X, fill=False, eps=0.5, ax=ax, alpha=.7)
    mglearn.discrete_scatter(X[:, 0], X[:, 1], y, ax=ax)
    ax.set_title("{}".format(clf.__class__.__name__))
    ax.set_xlabel("Признак 0")
    ax.set_ylabel("Признак 1")
axes[0].legend()
plt.show()

print("---------------------------")

# При низких С модели делают большой акцент на поиске w->0 (алгоритмы
# пытаются подстроиться под большинство точек данных). Невозможно правильно
# классифицировать все наблюдения этого набора данных с помощью прямой линии.
mglearn.plots.plot_linear_svc_regularization()
plt.show()

print("---------------------------")

# Коэффициенты, полученные с помощью логистической регрессии
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
cancer = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    cancer.data, cancer.target, stratify=cancer.target, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# Значение по умолчанию C=1 обеспечивает неплохое качество модели
# качество модели на обучающем и тестовом примерно одинаково->недообучили
logreg = LogisticRegression(max_iter=10000).fit(X_train_scaled, y_train)
print("Правильность на обучающем наборе: {:.3f}".format(logreg.score(X_train_scaled, y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(logreg.score(X_test_scaled, y_test)))

# П на обучающем и тестовом выше->более сложная модель должна сработать лучше
logreg100 = LogisticRegression(C=100, max_iter=10000).fit(X_train_scaled, y_train)
print("Правильность на обучающем наборе: {:.3f}".format(logreg100.score(X_train_scaled, y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(logreg100.score(X_test_scaled, y_test)))

# недообученная модель, П на обучающем и тестовом ниже, чем при С=1
logreg001 = LogisticRegression(C=0.01, max_iter=10000).fit(X_train_scaled, y_train)
print("Правильность на обучающем наборе: {:.3f}".format(logreg001.score(X_train_scaled, y_train)))
print("Правильность на тестовом наборе: {:.3f}".format(logreg001.score(X_test_scaled, y_test)))

plt.plot(logreg.coef_.T, 'o', label="C=1")
plt.plot(logreg100.coef_.T, '^', label="C=100")
plt.plot(logreg001.coef_.T, 'v', label="C=0.01")
plt.xticks(range(cancer.data.shape[1]), cancer.feature_names, rotation=90)
plt.hlines(0, 0, cancer.data.shape[1])
plt.ylim(-5, 5)
plt.xlabel("Индекс коэффициента")
plt.ylabel("Оценка коэффициента")
plt.legend()
plt.show()

print("---------------------------")

# Коэффициенты логистической регрессии с L1 штрафом для Breast Cancer
# основное различие между моделями – в параметре penalty, который влияет
# на регуляризацию и определяет, будет ли модель использовать все доступные
# признаки или выберет лишь подмножество признаков
for C, marker in zip([0.001, 1, 100], ['o', '^', 'v']):
    lr_l1 = LogisticRegression(C=C, penalty="l1", solver="liblinear", max_iter=10000).fit(X_train, y_train)
    print("Правильность на обучении для логрегрессии l1 с C={:.3f}: {:.2f}".format( C, lr_l1.score(X_train, y_train)))
    print("Правильность на тесте для логрегрессии l1 с C={:.3f}: {:.2f}".format( C, lr_l1.score(X_test, y_test)))
plt.plot(lr_l1.coef_.T, marker, label="C={:.3f}".format(C))
plt.xticks(range(cancer.data.shape[1]), cancer.feature_names, rotation=90)
plt.hlines(0, 0, cancer.data.shape[1])
plt.xlabel("Индекс коэффициента")
plt.ylabel("Оценка коэффициента")
plt.ylim(-5, 5)
plt.legend(loc=3)
plt.show()