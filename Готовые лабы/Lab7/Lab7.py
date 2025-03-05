friends = ['Valera Ryduak', 'Dashka Gluhova', 'Vladislav Lemeshevskiy', 'Nikita Turchinovich']
numbers = [1, 2.6, 5]
print(friends)
print(numbers)
print(friends[0]) 
print(numbers[-1])
print('---------------------Разложение списка-----------------------------------------')
valera, dasha, vlad, eminem = friends
print(eminem)
print('---------------------Перебор элементов (цикл for)------------------------------')
for friend in friends: 
    print(friend)
print('---------------------Перебор элементов (цикл while-----------------------------')
i = 0
while i < len(numbers):
    print(numbers[i])
    i += 1
print('---------------------Сравнение списков-----------------------------------------')
if friends == numbers: 
    print('Ok')
else:
    print('Списки не равны');
print('---------------------Вывод элементов списка------------------------------------')
slice_friends1 = friends[1:4:2] # Получение части списка с 1 по 4 с шагом 2
slice_friends2 = friends[:-1] # с предпоследнего по нулевой
slice_friends3 = friends[-2:-1] # со 2 с конца до предпоследний
print(slice_friends1)
print(slice_friends2)
print(slice_friends3)
print('---------------------Append, insert, extend, index, pop, remove, clear---------')
friends.append('Kostya') # Добавление в конец
friends.insert(5, 'Bill') # Добавить на 5 позицию
friends.extend(['Maksim', 'Tolya']) # Добавление набора элементов
print(friends)
index_of_kostya = friends.index('Kostya') # Получение индекса элемента
print(index_of_kostya)
removed_item = friends.pop(index_of_kostya) # Удаление по индексу
print(removed_item)
last_item = friends.pop() # Удаление последнего элемента
print(last_item)
friends.remove('Valera Ryduak') # Удаление элемента
print(friends)
#friends.clear()
print('---------------------Удаление элемента-----------------------------------------')
if 'Dashka Gluhova' in friends:
    friends.remove('Dashka Gluhova')
print(friends)
print('---------------------Удаление по 2 элемент-------------------------------------')
del numbers[:1]
print(numbers)
print('---------------------Подсчет вхождений-----------------------------------------')
friend_count = friends.count('Vladislav Lemeshevskiy')
print(friend_count)
print('---------------------Сортировка (методы sort и reverse)------------------------')
people = ['Valera Ryduak', 'Dashka Gluhova', 'Vladislav Lemeshevskiy', 'Nikita Turchinovich']
people.sort(key=str.lower)
people.reverse()
print(people)
print('---------------------Сортировка (метод sorted)---------------------------------')
sorted_people = sorted(people, key=str.lower)
print(sorted_people)
print('---------------------Фильтрация списка-----------------------------------------')
numbers = [-5, -2, -1, 0, 1, 2, 5] # Фильтрация списка
def condition(number): return number > 0
result = filter(condition, numbers)
#result = filter(lambda n: n > 1, numbers)
for n in result: print(n, end=' ')
print('\n---------------------Преобразование списка-------------------------------------')
numbers = [ 1, 2, 3, 4, 5]
#def square(number): return number * number
result = map(lambda n: n*n, numbers)
for n in result: print(n, end=" ")
print('\n')
print(min(numbers))
print(max(numbers))
print('---------------------Указывает на один и тот же список-------------------------')
numbers1 = [ 1, 2, 3, 4, 5]
numbers2 = numbers1
numbers2.append(6)
print(numbers1)
print(numbers2)
print('---------------------Копирование (copy), добавление, соединение списков--------')
numbers3 = numbers1.copy()
numbers3.append(7)
print(numbers3)
numbers4 = numbers1 + numbers2
print(numbers4)
print('------------------------------КОРТЕЖИ------------------------------------------')
kfc = 'kfc', 30 # Или можем со скобками
print(kfc)
tuple1 = tuple(numbers4) # Создание кортежа из списка
print(tuple1)
print(len(tuple1)) # Длина кортежа
print(tuple1[-1]) # С конца списка
kfc, age = 'kfc', 40 # Разложение кортежа
print(kfc)
print(age)
print(tuple1[1:3]) # С 1 по 3 элемент
print(tuple1[:3]) # С 0 по 3 элемент
print(tuple1[1:]) # С первого по последний элемент
print('---------------------Возврат зачений из функции (кортеж)----------------------')
def my_people():
    name = 'Mef'
    age = 20
    return name, age

people = my_people()
print(people)
print('------------------------------СЛОВАРИ-----------------------------------------')
users = {1: 'Dasha', 2: 'Sveta', 3: 'Lera'}
print(users)
print('---------------------Преобразование списков-----------------------------------')
user_list = [
    ['dasha@gmail.com', 'Dasha'],
    ['sveta@gmail.com', 'Sveta'],
    ['lera@gmail.com', 'Lera']
]
user_dict = dict(user_list) # Можно преобразовать так же и кортежи
print(user_dict)
print(user_dict['sveta@gmail.com'])
user_dict['dasha@gmail.com'] = 'Gluhova'
print(user_dict)
print('---------------------Получаем элемент (по ключу)-------------------------------')
key = 2
if key in users:
    user = users[key]
    print(user)
else:
    print('Элемент с таким ключом не найден')
print('---------------------Получаем элемент (метод get)------------------------------')
user1 = user_dict.get('sveta@gmail.com', 'Unknown user')
print(user1)
print('---------------------Удаляем элемент с ключом 3 (оператор del)-----------------')
key = 3
if key in users:  
    del users[key]
    print(f'Элемент с ключом {key} удален')
else:
    print('Элемент с таким ключом не найден')
print('---------------------Удаляем элемент (метод pop)-------------------------------')
user2 = user_dict.pop('sveta@gmail.com', 'Unknown user')
print(user2)
#user_dict.clear()
print('---------------------Копирует, возвращая новый словарь (метод copy)------------')
students = users.copy()
print(students)
print('---------------------Объединение двух словарей (метод update)------------------')
students.update(user_dict)
print(students)
print('---------------------Перебор словаря (цикл for)--------------------------------')
for key in users:
    print(f'Key: {key}, Name: {users[key]}')
print('---------------------Перебор словаря (метод items)-----------------------------')
for key, value in users.items():
    print(f'Key: {key}, Name: {value}')
print('---------------------Перебор ключей (метод keys)-------------------------------')
for key in users.keys():
    print(key)
print('---------------------Перебор значений (метод values)---------------------------')
for value in users.values():
    print(value)
