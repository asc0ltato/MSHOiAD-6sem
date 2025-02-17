CREATE TABLE Status (
    Status_ID NUMBER PRIMARY KEY,
    Status_Name VARCHAR2(50)
);

CREATE TABLE Role (
    Role_ID NUMBER PRIMARY KEY,
    Role_Name VARCHAR2(50)
);

CREATE TABLE Cars (
    Car_ID NUMBER PRIMARY KEY,
    Status_ID NUMBER,
    Brand VARCHAR2(255),
    Model VARCHAR2(255),
    YearOf NUMBER,
    License_Plate VARCHAR2(20) UNIQUE,
    Rental_Price NUMBER(10, 2),
    Location VARCHAR2(255),
    FOREIGN KEY (Status_ID) REFERENCES Status(Status_ID)
);

CREATE TABLE Users (
    User_ID NUMBER PRIMARY KEY,
    Role_ID NUMBER,
    First_Name VARCHAR2(50),
    Last_Name VARCHAR2(50),
    Address VARCHAR2(255),
    Phone_Number VARCHAR2(15),
    Email VARCHAR2(255) UNIQUE,
    Drivers_License VARCHAR2(20),
    FOREIGN KEY (Role_ID) REFERENCES Role(Role_ID)
);

CREATE TABLE Payments (
    Payment_ID NUMBER PRIMARY KEY,
    Payment_Amount NUMBER(10, 2),
    Payment_Date DATE,
    Payment_Method VARCHAR2(50)
);

CREATE TABLE Orders (
    Order_ID NUMBER PRIMARY KEY,
    User_ID NUMBER,
    Car_ID NUMBER,
    Payment_ID NUMBER,
    Start_DateTime DATE,
    End_DateTime DATE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Car_ID) REFERENCES Cars(Car_ID),
    FOREIGN KEY (Payment_ID) REFERENCES Payments(Payment_ID)
);
------------------------------------------------------------------------------
CREATE SEQUENCE seq_User_ID START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_Payment_ID START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_Order_ID START WITH 1 INCREMENT BY 1 NOCACHE;
CREATE SEQUENCE seq_Car_ID START WITH 1 INCREMENT BY 1 NOCACHE;
------------------------------------------------------------------------------
INSERT INTO Status (Status_ID, Status_Name) VALUES (1, 'Доступен');
INSERT INTO Status (Status_ID, Status_Name) VALUES (2, 'Арендован');
INSERT INTO Status (Status_ID, Status_Name) VALUES (3, 'В ремонте');
------------------------------------------------------------------------------
INSERT INTO Role (Role_ID, Role_Name) VALUES (1, 'Guest');
INSERT INTO Role (Role_ID, Role_Name) VALUES (2, 'User');
INSERT INTO Role (Role_ID, Role_Name) VALUES (3, 'Manager');
INSERT INTO Role (Role_ID, Role_Name) VALUES (4, 'Admin');
------------------------------------------------------------------------------
INSERT INTO Cars (Car_ID, Status_ID, Brand, Model, YearOf, License_Plate, Rental_Price, Location)
VALUES (seq_Car_ID.NEXTVAL, 1, 'Toyota', 'Camry', 2020, 'А123ВС77', 120.50, 'г.Минск, ул. Белорусская, д.19');
INSERT INTO Cars (Car_ID, Status_ID, Brand, Model, YearOf, License_Plate, Rental_Price, Location)
VALUES (seq_Car_ID.NEXTVAL, 2, 'Hyundai', 'Solaris', 2019, 'В456АС77', 100.99, 'г.Минск, ул. Казинца, д.23');
INSERT INTO Cars (Car_ID, Status_ID, Brand, Model, YearOf, License_Plate, Rental_Price, Location)
VALUES (seq_Car_ID.NEXTVAL, 3, 'BMW', 'X5', 2021, 'С789ДА77', 130.99, 'г.Минск, ул. Свердлова, д.11');
INSERT INTO Cars (Car_ID, Status_ID, Brand, Model, YearOf, License_Plate, Rental_Price, Location)
VALUES (seq_Car_ID.NEXTVAL, 1, 'Audi', 'A6', 2015, 'Е987МК77', 80.00, 'г.Минск, ул. Петра Глебки, д.9');
INSERT INTO Cars (Car_ID, Status_ID, Brand, Model, YearOf, License_Plate, Rental_Price, Location)
VALUES (seq_Car_ID.NEXTVAL, 2, 'Mercedes', 'C-Class', 2022, 'Р654ОМ77', 150.00, 'г.Минск, ул. Белорусская, д.19');
------------------------------------------------------------------------------
INSERT INTO Users (User_ID, Role_ID, First_Name, Last_Name, Address, Phone_Number, Email, Drivers_License)
VALUES (seq_User_ID.NEXTVAL, 4, 'Иван', 'Иванов', 'г.Минск, ул. Независимость, д.20', '+37560000001', 'ivanov@mail.ru', NULL);
INSERT INTO Users (User_ID, Role_ID, First_Name, Last_Name, Address, Phone_Number, Email, Drivers_License)
VALUES (seq_User_ID.NEXTVAL, 2, 'Ольга', 'Петрова', 'г.Минск, ул. Партизанская, д.15', '+37560000002', 'petrova@mail.ru', '7800222333');
INSERT INTO Users (User_ID, Role_ID, First_Name, Last_Name, Address, Phone_Number, Email, Drivers_License)
VALUES (seq_User_ID.NEXTVAL, 3, 'Алексей', 'Сидоров', 'г.Минск, ул. Киселева, д.13', '+37560000003', 'sidorov@mail.ru', NULL);
INSERT INTO Users (User_ID, Role_ID, First_Name, Last_Name, Address, Phone_Number, Email, Drivers_License)
VALUES (seq_User_ID.NEXTVAL, 3, 'Мария', 'Васильева', 'г.Минск, ул. Жудра, д.50', '+37560000004', 'vasilieva@mail.ru', NULL);
INSERT INTO Users (User_ID, Role_ID, First_Name, Last_Name, Address, Phone_Number, Email, Drivers_License)
VALUES (seq_User_ID.NEXTVAL, 2, 'Дмитрий', 'Козлов', 'г.Минск, ул. Кижеватова, д.26', '+37560000005', 'kozlov@mail.ru', '7400555666');
------------------------------------------------------------------------------
INSERT INTO Payments (Payment_ID, Payment_Amount, Payment_Date, Payment_Method)
VALUES (seq_Payment_ID.NEXTVAL, 28920.00, TO_DATE('2024-09-10', 'YYYY-MM-DD'), 'Карта');
INSERT INTO Payments (Payment_ID, Payment_Amount, Payment_Date, Payment_Method)
VALUES (seq_Payment_ID.NEXTVAL, 24237.60, TO_DATE('2024-09-15', 'YYYY-MM-DD'), 'Наличка');
INSERT INTO Payments (Payment_ID, Payment_Amount, Payment_Date, Payment_Method)
VALUES (seq_Payment_ID.NEXTVAL, 31437.60, TO_DATE('2024-09-20', 'YYYY-MM-DD'), 'Наличка');
INSERT INTO Payments (Payment_ID, Payment_Amount, Payment_Date, Payment_Method)
VALUES (seq_Payment_ID.NEXTVAL, 19200.00, TO_DATE('2024-09-25', 'YYYY-MM-DD'), 'Карта');
INSERT INTO Payments (Payment_ID, Payment_Amount, Payment_Date, Payment_Method)
VALUES (seq_Payment_ID.NEXTVAL, 36000.00, TO_DATE('2024-09-30', 'YYYY-MM-DD'), 'Карта');
------------------------------------------------------------------------------
INSERT INTO Orders (Order_ID, User_ID, Car_ID, Payment_ID, Start_DateTime, End_DateTime)
VALUES (seq_Order_ID.NEXTVAL, 2, 1, 2, TO_DATE('2024-09-01', 'YYYY-MM-DD'), TO_DATE('2024-09-10', 'YYYY-MM-DD'));
INSERT INTO Orders (Order_ID, User_ID, Car_ID, Payment_ID, Start_DateTime, End_DateTime)
VALUES (seq_Order_ID.NEXTVAL, 5, 2, 3, TO_DATE('2024-09-05', 'YYYY-MM-DD'), TO_DATE('2024-09-15', 'YYYY-MM-DD'));
INSERT INTO Orders (Order_ID, User_ID, Car_ID, Payment_ID, Start_DateTime, End_DateTime)
VALUES (seq_Order_ID.NEXTVAL, 4, 3, 2, TO_DATE('2024-09-10', 'YYYY-MM-DD'), TO_DATE('2024-09-20', 'YYYY-MM-DD'));
INSERT INTO Orders (Order_ID, User_ID, Car_ID, Payment_ID, Start_DateTime, End_DateTime)
VALUES (seq_Order_ID.NEXTVAL, 2, 4, 3, TO_DATE('2024-09-15', 'YYYY-MM-DD'), TO_DATE('2024-09-25', 'YYYY-MM-DD'));
INSERT INTO Orders (Order_ID, User_ID, Car_ID, Payment_ID, Start_DateTime, End_DateTime)
VALUES (seq_Order_ID.NEXTVAL, 5, 5, 1, TO_DATE('2024-09-20', 'YYYY-MM-DD'), TO_DATE('2024-09-30', 'YYYY-MM-DD'));
-- Представление для доступных автомобилей
CREATE OR REPLACE VIEW AvailableCars AS
SELECT
    Car_ID,
    Brand,
    Model,
    YearOf,
    License_Plate,
    Rental_Price,
    Location
FROM Cars
WHERE Status_ID = 1;

-- Просмотр данных из представления AvailableCars
SELECT * FROM AvailableCars;
-- Представление длz просмотров заказов
CREATE OR REPLACE VIEW OrderDetails AS
SELECT
    O.Order_ID,
    U.First_Name,
    U.Last_Name,
    C.Brand,
    C.Model,
    C.License_Plate,
    O.Start_DateTime,
    O.End_DateTime,
    P.Payment_Amount,
    P.Payment_Method
FROM Orders O
JOIN Users U ON O.User_ID = U.User_ID
JOIN Cars C ON O.Car_ID = C.Car_ID
JOIN Payments P ON O.Payment_ID = P.Payment_ID;
-- Просмотр данных из представления OrderDetails
SELECT * FROM OrderDetails;

CREATE INDEX idx_Users_LastName_FirstName ON Users(Last_Name, First_Name);
CREATE INDEX idx_Users_DriversLicence ON Users(Drivers_License);
CREATE INDEX idx_Cars_Brand_Model ON Cars(Brand, Model);

-- Функция для расчета общей суммы арендных платежей
CREATE OR REPLACE FUNCTION GetTotalRentalPayments(p_User_ID NUMBER) RETURN NUMBER IS
v_Total NUMBER;
BEGIN
    SELECT SUM(P.Payment_Amount) INTO v_Total
    FROM Payments P
    JOIN Orders O ON P.Payment_ID = O.Payment_ID
    WHERE O.User_ID = p_User_ID;
    RETURN NVL(v_Total, 0); 
END;

-- Процедура для создание нового заказа
CREATE OR REPLACE PROCEDURE InsertOrder (
    p_UserID IN NUMBER,
    p_CarID IN NUMBER,
    p_PaymentAmount IN NUMBER,
    p_PaymentDate IN DATE,
    p_PaymentMethod IN VARCHAR2,
    p_StartDateTime IN DATE,
    p_EndDateTime IN DATE
) AS
v_PaymentID NUMBER;
BEGIN
    IF EXISTS (
    SELECT 1
    FROM Orders
    WHERE Car_ID = p_CarID
    AND (Start_DateTime < p_EndDateTime AND End_DateTime > p_StartDateTime)
    ) THEN
    RAISE_APPLICATION_ERROR(-20001, 'Автомобиль недоступен на указанные даты');
    END IF;

    INSERT INTO Payments (Payment_ID, Payment_Amount, Payment_Date, Payment_Method)
    VALUES (seq_Payment_ID.NEXTVAL, p_PaymentAmount, p_PaymentDate, p_PaymentMethod);
    
    SELECT seq_Payment_ID.CURRVAL INTO v_PaymentID FROM dual;
    
    INSERT INTO Orders (Order_ID, User_ID, Car_ID, Payment_ID, Start_DateTime, End_DateTime)
    VALUES (seq_Order_ID.NEXTVAL, p_UserID, p_CarID, v_PaymentID, p_StartDateTime, p_EndDateTime);
END;

CREATE OR REPLACE TRIGGER trg_CheckOrderDates
BEFORE INSERT OR UPDATE ON Orders
FOR EACH ROW
BEGIN
    IF :NEW.End_DateTime < :NEW.Start_DateTime THEN
    RAISE_APPLICATION_ERROR(-20002, 'Дата окончания аренды не может быть раньше даты начала.');
    END IF;
END;

CREATE OR REPLACE TRIGGER trg_CheckDuplicatePayment
BEFORE INSERT ON Payments
FOR EACH ROW
    DECLARE
    v_Count NUMBER;
    BEGIN
    SELECT COUNT(*) INTO v_Count
    FROM Payments p
    WHERE p.Payment_Amount = :NEW.Payment_Amount
    AND p.Payment_Date = :NEW.Payment_Date
    AND p.Payment_Method = :NEW.Payment_Method;

    IF v_Count > 0 THEN
    RAISE_APPLICATION_ERROR(-20001, 'Платеж с такими же данными уже существует');
    END IF;
END;

CREATE OR REPLACE TRIGGER trg_AutoUpdateCarStatus
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
    UPDATE Cars
    SET Status_ID = 2
    WHERE Car_ID = :NEW.Car_ID;
END;
