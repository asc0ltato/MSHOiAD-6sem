create database Rent;
use Rent;
--drop database Rent;
--drop table Status;
--drop table Role;
--drop table Cars;
--drop table Users;
--drop table Payments;
--drop table Orders;

CREATE TABLE Status (
    Status_ID INT PRIMARY KEY,
    Status_Name VARCHAR(50)
);

CREATE TABLE Role (
    Role_ID INT PRIMARY KEY,
    Role_Name VARCHAR(50)
);

CREATE TABLE Cars (
    Car_ID INT PRIMARY KEY,
	Status_ID INT,
	Brand VARCHAR(255),
    Model VARCHAR(255),
    YearOf INT,
	License_Plate VARCHAR(20),
    Rental_Price DECIMAL(10, 2),
    Location VARCHAR(255),
    FOREIGN KEY (Status_id) REFERENCES Status(Status_ID)
);

CREATE TABLE Users (
    User_ID INT PRIMARY KEY,
	Role_ID INT,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Address VARCHAR(255),
    Phone_Number VARCHAR(15),
    Email VARCHAR(255) UNIQUE,
    Drivers_License VARCHAR(20)
	FOREIGN KEY (Role_ID) REFERENCES Role(Role_ID)
);

CREATE TABLE Payments (
    Payment_ID INT PRIMARY KEY,
    Payment_Amount DECIMAL(10, 2),
    Payment_Date DATE,
	Payment_Method VARCHAR(50)
);

CREATE TABLE Orders (
    Order_ID INT PRIMARY KEY,
	User_ID INT,
	Car_ID INT,
    Payment_ID INT,
    Start_DateTime DATE,
    End_DateTime DATE,
    FOREIGN KEY (User_ID) REFERENCES Users(User_ID),
    FOREIGN KEY (Car_ID) REFERENCES Cars(Car_ID),
    FOREIGN KEY (Payment_ID) REFERENCES Payments(Payment_ID)
);

select * from Status;
select * from Role;
select * from Cars;
select * from Users;
select * from Orders;
select * from Payments;

CREATE SEQUENCE seq_User_ID
START WITH 1
INCREMENT BY 1
NO CACHE;  
 
CREATE SEQUENCE seq_Payment_ID
START WITH 1
INCREMENT BY 1
NO CACHE; 

CREATE SEQUENCE seq_Order_ID
START WITH 1
INCREMENT BY 1
NO CACHE; 

CREATE SEQUENCE seq_Car_ID
START WITH 1
INCREMENT BY 1
NO CACHE; 

INSERT INTO Status (Status_ID, Status_Name)
VALUES 
(1, 'Доступен'),
(2, 'Арендован'),
(3, 'В ремонте');

INSERT INTO Role (Role_ID, Role_Name)
VALUES 
(1, 'Guest'),
(2, 'User'),
(3, 'Manager'),
(4, 'Admin');

INSERT INTO Cars (Car_ID, Status_ID, Brand, Model, YearOf, License_Plate, Rental_Price, Location)
VALUES 
(NEXT VALUE FOR seq_Car_ID, 1, 'Toyota', 'Camry', 2020, 'А123ВС77', 120.50, 'г. Минск, ул. Белорусская, д.19'),
(NEXT VALUE FOR seq_Car_ID, 2, 'Hyundai', 'Solaris', 2019, 'В456АС77', 100.99, 'г. Минск, ул. Казинца, д.23'),
(NEXT VALUE FOR seq_Car_ID, 3, 'BMW', 'X5', 2021, 'С789ДА77', 130.99, 'г. Минск, ул. Свердлова, д.11'),
(NEXT VALUE FOR seq_Car_ID, 1, 'Audi', 'A6', 2015, 'Е987МК77', 80.00, 'г. Минск, ул. Петра Глебки, д.9'),
(NEXT VALUE FOR seq_Car_ID, 2, 'Mercedes', 'C-Class', 2022, 'Р654ОМ77', 150.00, 'г. Минск, ул. Белорусская, д.19');

INSERT INTO Users (User_ID, Role_ID, First_Name, Last_Name, Address, Phone_number, Email, Drivers_license)
VALUES 
(NEXT VALUE FOR seq_User_ID, 4, 'Иван', 'Иванов', 'г.Минск, ул. Независимость, д.20', '+37560000001', 'ivanov@mail.ru', NULL),
(NEXT VALUE FOR seq_User_ID, 2, 'Ольга', 'Петрова', 'г.Минск, ул. Партизанская, д.15', '+37560000002', 'petrova@mail.ru', '7800222333'),
(NEXT VALUE FOR seq_User_ID, 3, 'Алексей', 'Сидоров', 'г.Минск, ул. Киселева, д.13', '+37560000003', 'sidorov@mail.ru', NULL),
(NEXT VALUE FOR seq_User_ID, 3, 'Мария', 'Васильева', 'г.Минск, ул. Жудра, д.50', '+37560000004', 'vasilieva@mail.ru', NULL),
(NEXT VALUE FOR seq_User_ID, 2, 'Дмитрий', 'Козлов', 'г.Минск, ул. Кижеватова, д.26', '+37560000005', 'kozlov@mail.ru', '7400555666');

INSERT INTO Payments (Payment_ID, Payment_Amount, Payment_Date, Payment_Method)
VALUES 
(NEXT VALUE FOR seq_Payment_ID, 28920.00, '2024-09-10', 'Карта'),
(NEXT VALUE FOR seq_Payment_ID, 24237.60, '2024-09-15', 'Наличные'),
(NEXT VALUE FOR seq_Payment_ID, 31437.60, '2024-09-20', 'Наличные'),
(NEXT VALUE FOR seq_Payment_ID, 19200.00, '2024-09-25', 'Карта'),
(NEXT VALUE FOR seq_Payment_ID, 36000.00, '2024-09-30', 'Карта');

INSERT INTO Orders (Order_ID, User_ID, Car_ID, Payment_ID, Start_DateTime, End_DateTime)
VALUES 
(NEXT VALUE FOR seq_Order_ID, 2, 1, 2, '2024-09-01', '2024-09-10'),
(NEXT VALUE FOR seq_Order_ID, 5, 2, 3, '2024-09-05', '2024-09-15'),
(NEXT VALUE FOR seq_Order_ID, 4, 3, 2, '2024-09-10', '2024-09-20'),
(NEXT VALUE FOR seq_Order_ID, 2, 4, 3, '2024-09-15', '2024-09-25'),
(NEXT VALUE FOR seq_Order_ID, 5, 5, 1, '2024-09-20', '2024-09-30');