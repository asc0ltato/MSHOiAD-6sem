--2.	Продемонстрировать обработку данных из объектных таблиц при помощи 
--коллекций следующим образом по варианту (в каждом варианте первая таблица t1, 
--вторая – t2):
--a.	Создать коллекцию на основе t1, далее K1, для нее как атрибут – 
--вложенную коллекцию на основе t2, далее К2;
--b.	Выяснить для каких коллекций К1 коллекции К2 пересекаются;
--c.	Выяснить, является ли членом коллекции К1 какой-то произвольный элемент;
--d.	Найти пустые коллекции К1;
--e.	Для двух элементов коллекции К1 обменять их атрибуты К2. 

-- Создание типа объекта для коллекции
CREATE OR REPLACE TYPE CarType AS OBJECT (
    Car_ID NUMBER,
    Status_ID NUMBER,
    Brand VARCHAR2(50),
    Model VARCHAR2(50),
    YearOf NUMBER,
    License_Plate VARCHAR2(20),
    Rental_Price NUMBER,
    Location VARCHAR2(50)
);

-- Создание коллекции объектов типа CarType
CREATE OR REPLACE TYPE CarTableType IS TABLE OF CarType;

CREATE OR REPLACE TYPE OrderType AS OBJECT (
    Order_ID NUMBER,
    User_ID NUMBER,
    Payment_ID NUMBER,
    Start_DateTime DATE,
    End_DateTime DATE,
    Cars CarTableType
);

CREATE OR REPLACE TYPE OrderTableType IS TABLE OF OrderType;

DROP TYPE OrderTableType;
DROP TYPE OrderType;
DROP TYPE CarTableType;
DROP TYPE CarType;

DECLARE
    -- Создание ассоциативных массивов
    TYPE OrderArray IS TABLE OF Orders%ROWTYPE INDEX BY PLS_INTEGER;
    TYPE CarArray IS TABLE OF Cars%ROWTYPE INDEX BY PLS_INTEGER;
    
    K1 OrderTableType := OrderTableType();
    K2 CarTableType := CarTableType();
    v_Orders OrderArray;
    v_Cars CarArray;
    v_Exists INTEGER := 0;  
    v_inserted INTEGER := 0;
    v_updated INTEGER := 0;
BEGIN
    -- a. Заполняем коллекцию K1 (Orders) и вложенную коллекцию K2 (Cars)    
    SELECT * BULK COLLECT INTO v_Orders FROM Orders; -- Вставка данных из таблиц в массив
    SELECT * BULK COLLECT INTO v_Cars FROM Cars;
    
    FOR i IN 1 .. v_Orders.COUNT LOOP
        K2.DELETE; -- Удаление коллекции для предотвращения ошибок
        FOR j IN 1 .. v_Cars.COUNT LOOP
            IF v_Cars(j).Car_ID = v_Orders(i).Car_ID THEN
                K2.EXTEND; -- Расширение коллекции
                K2(K2.LAST) := CarType(v_Cars(j).Car_ID, v_Cars(j).Status_ID, 
                                       v_Cars(j).Brand, v_Cars(j).Model, 
                                       v_Cars(j).YearOf, v_Cars(j).License_Plate, 
                                       v_Cars(j).Rental_Price, v_Cars(j).Location);
            END IF;
        END LOOP;
        
        K1.EXTEND;
        K1(K1.LAST) := OrderType(v_Orders(i).Order_ID, v_Orders(i).User_ID, 
                                 v_Orders(i).Payment_ID, v_Orders(i).Start_DateTime, 
                                 v_Orders(i).End_DateTime, K2);
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('Данные загружены в коллекции K1 и K2');
    
    -- b. Проверяем пересечение вложенных коллекций K2
    FOR i IN 1 .. K1.COUNT LOOP
        FOR j IN 1 .. K1(i).Cars.COUNT LOOP
            FOR k IN i+1 .. K1.COUNT LOOP -- С i+1, чтобы избежать повторных сравнений
                FOR m IN 1 .. K1(k).Cars.COUNT LOOP
                    IF K1(i).Cars(j).Car_ID = K1(k).Cars(m).Car_ID THEN
                        DBMS_OUTPUT.PUT_LINE('Пересечение: Car_ID = ' || 
                        K1(i).Cars(j).Car_ID);
                    END IF;
                END LOOP;
            END LOOP;
        END LOOP;
    END LOOP;
    
    -- c. Проверяем, является ли элемент членом коллекции K1
    FOR i IN 1 .. K1.COUNT LOOP
        IF K1(i).Order_ID = 2 THEN
            v_Exists := 1;
            EXIT;
        END IF;
    END LOOP;
    IF v_Exists = 1 THEN
        DBMS_OUTPUT.PUT_LINE('Order_ID 2 найден в коллекции K1');
    ELSE
        DBMS_OUTPUT.PUT_LINE('Order_ID 2 не найден в коллекции K1');
    END IF;
    
    -- d. Поиск пустых коллекций K1
    FOR i IN 1 .. K1.COUNT LOOP
        IF K1(i).Cars.COUNT = 0 THEN
            DBMS_OUTPUT.PUT_LINE('Пустая коллекция K1: Order_ID = ' 
            || K1(i).Order_ID);
        END IF;
    END LOOP;
    
    -- e. Обмен атрибутами K2 между двумя элементами K1
    IF K1.COUNT > 1 THEN
        DECLARE
            temp_Cars CarTableType;
        BEGIN
            DBMS_OUTPUT.PUT_LINE('До обмена:');
            FOR i IN 1 .. K1(4).Cars.COUNT LOOP
                DBMS_OUTPUT.PUT_LINE('K1(4).Cars(' || i || ') = ' || K1(4).Cars(i).Car_ID);
            END LOOP;   
            
            FOR i IN 1 .. K1(5).Cars.COUNT LOOP
                DBMS_OUTPUT.PUT_LINE('K1(5).Cars(' || i || ') = ' || K1(5).Cars(i).Car_ID);
            END LOOP;

            temp_Cars := K1(4).Cars;
            K1(4).Cars := K1(5).Cars;
            K1(5).Cars := temp_Cars;
            
            DBMS_OUTPUT.PUT_LINE('После обмена:');
            FOR i IN 1 .. K1(4).Cars.COUNT LOOP
                DBMS_OUTPUT.PUT_LINE('K1(4).Cars(' || i || ') = ' || K1(4).Cars(i).Car_ID);
            END LOOP;
            
            FOR i IN 1 .. K1(5).Cars.COUNT LOOP
                DBMS_OUTPUT.PUT_LINE('K1(5).Cars(' || i || ') = ' || K1(5).Cars(i).Car_ID);
            END LOOP;
            
            DBMS_OUTPUT.PUT_LINE('Обмен атрибутами K2 между K1(4) и K1(5) сделан');
        END;
    END IF;
    
    -- 3. Преобразование коллекции в реляционные данные
    FOR i IN 1 .. K1.COUNT LOOP
        FOR j IN 1 .. K1(i).Cars.COUNT LOOP
            BEGIN
                DECLARE
                    v_exists INTEGER;
                BEGIN
                    SELECT COUNT(*) INTO v_exists FROM t1 WHERE Car_ID = K1(i).Cars(j).Car_ID;
                    IF v_exists = 0 THEN
                        INSERT INTO t1 (Car_ID, Status_ID, Brand, Model, YearOf, License_Plate, Rental_Price, Location)
                        VALUES (K1(i).Cars(j).Car_ID, K1(i).Cars(j).Status_ID, K1(i).Cars(j).Brand, 
                                K1(i).Cars(j).Model, K1(i).Cars(j).YearOf, K1(i).Cars(j).License_Plate, 
                                K1(i).Cars(j).Rental_Price, K1(i).Cars(j).Location);
                        v_inserted := v_inserted + 1; 
                    ELSE
                        DBMS_OUTPUT.PUT_LINE('Ошибка: Car_ID ' || K1(i).Cars(j).Car_ID || ' уже существует');
                    END IF;
                END;
            END;
        END LOOP;
    END LOOP;
    
    DBMS_OUTPUT.PUT_LINE('Количество вставленных данных: ' || v_inserted);
    
    -- 4. Применение BULK операций
    BEGIN
    -- FORALL обновляет все записи Orders за 1 запрос быстрее, чем FOR и UPDATE
    FORALL i IN INDICES OF K1  -- INDICES OF K1 перебирает все индексы массива K1
        UPDATE Orders
        SET User_ID = K1(i).User_ID, 
            Payment_ID = 1, 
            Start_DateTime = K1(i).Start_DateTime, 
            End_DateTime = K1(i).End_DateTime
        WHERE Order_ID = K1(i).Order_ID;

    v_updated := SQL%ROWCOUNT;

    FOR i IN 1 .. K1.COUNT LOOP
        FORALL j IN INDICES OF K1(i).Cars
            UPDATE Cars
            SET Status_ID = K1(i).Cars(j).Status_ID, 
                Brand = K1(i).Cars(j).Brand, 
                Model = K1(i).Cars(j).Model, 
                YearOf = K1(i).Cars(j).YearOf, 
                License_Plate = K1(i).Cars(j).License_Plate, 
                Rental_Price = 100, 
                Location = K1(i).Cars(j).Location
            WHERE Car_ID = K1(i).Cars(j).Car_ID;

        v_updated := v_updated + SQL%ROWCOUNT;
    END LOOP;
    DBMS_OUTPUT.PUT_LINE('Успешно обновлено записей: ' || v_updated);
    EXCEPTION
        WHEN OTHERS THEN
            DBMS_OUTPUT.PUT_LINE('Ошибка: ' || SQLERRM);
    END;
END;

CREATE TABLE t1 (
    Car_ID NUMBER,
    Status_ID NUMBER,
    Brand VARCHAR2(50),
    Model VARCHAR2(50),
    YearOf NUMBER,
    License_Plate VARCHAR2(20),
    Rental_Price NUMBER,
    Location VARCHAR2(50)
);

DROP TABLE t1;

SELECT * FROM Orders;
SELECT * FROM Cars;