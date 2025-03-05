CREATE DATABASE CarRentalDWH;
GO
USE CarRentalDWH;
GO

CREATE TABLE DimUsers (
    User_ID INT PRIMARY KEY,
    First_Name NVARCHAR(50),
    Last_Name NVARCHAR(50),
    Role_Name NVARCHAR(50),
	Address VARCHAR(255),
    Phone_Number VARCHAR(15),
    Email VARCHAR(255) UNIQUE,
    Drivers_License VARCHAR(20)
);

CREATE TABLE DimCars (
    Car_ID INT PRIMARY KEY,
    Brand NVARCHAR(255),
    Model NVARCHAR(255),
    YearOf INT,
	License_Plate VARCHAR(20),
    Status_Name NVARCHAR(50),
	Rental_Price DECIMAL(10,2),
	Location VARCHAR(255)
);

CREATE TABLE DimPayments (
    Payment_ID INT PRIMARY KEY,
    Payment_Method NVARCHAR(50),
	Payment_Amount DECIMAL(10,2)
);

CREATE TABLE DimTime (
    Date_ID INT PRIMARY KEY,
    FullDate DATE
);


CREATE TABLE FactOrders (
    Order_ID INT PRIMARY KEY,
    User_ID INT,
    Car_ID INT,
    Payment_ID INT,
    Date_ID INT,
    Start_Date DATE,
    End_Date DATE,
    FOREIGN KEY (User_ID) REFERENCES DimUsers(User_ID),
    FOREIGN KEY (Car_ID) REFERENCES DimCars(Car_ID),
    FOREIGN KEY (Payment_ID) REFERENCES DimPayments(Payment_ID),
    FOREIGN KEY (Date_ID) REFERENCES DimTime(Date_ID)
);

-- Вставка данных в таблицу DimUsers
INSERT INTO DimUsers (User_ID, First_Name, Last_Name, Role_Name, Address, Phone_Number, Email, Drivers_License) 
VALUES
(1, 'Иван', 'Иванов', 'Admin', 'ул. Независимости, Минск', '8(017)123-45-67', 'ivan.ivanov@email.com', 'AB1234567'),
(2, 'Алена', 'Смирнова', 'Manager', 'ул. Ленина, Брест', '8(016)234-56-78', 'alena.smirnova@email.com', 'BC2345678'),
(3, 'Андрей', 'Ковалев', 'Customer', 'ул. Гагарина, Гомель', '8(023)345-67-89', 'andrey.kovalev@email.com', 'CD3456789'),
(4, 'Екатерина', 'Петрова', 'Customer', 'пр. Победы, Витебск', '8(021)456-78-90', 'ekaterina.petrov@email.com', 'DE4567890'),
(5, 'Михаил', 'Михайлов', 'Manager', 'ул. Бобруйская, Гродно', '8(015)567-89-01', 'mikhail.mikhaylov@email.com', 'EF5678901'),
(6, 'Светлана', 'Сидорова', 'Admin', 'пр. Мира, Минск', '8(017)678-90-12', 'svetlana.sidorova@email.com', 'FG6789012'),
(7, 'Дмитрий', 'Дмитриев', 'Customer', 'ул. Чкалова, Могилев', '8(022)789-01-23', 'dmitriy.dmitriev@email.com', 'GH7890123'),
(8, 'Марина', 'Кузнецова', 'Customer', 'ул. Кирова, Пинск', '8(016)890-12-34', 'marina.kuznetsova@email.com', 'HI8901234');

-- Вставка данных в таблицу DimCars
INSERT INTO DimCars (Car_ID, Brand, Model, YearOf, License_Plate, Status_Name, Rental_Price, Location)
VALUES
(1, 'Toyota', 'Camry', 2020, 'ABC1234', 'Available', 350.00, 'Downtown'),
(2, 'Honda', 'Civic', 2019, 'DEF5678', 'Available', 200.00, 'Suburbs'),
(3, 'Ford', 'Fusion', 2021, 'GHI9101', 'Rented', 450.00, 'Airport'),
(4, 'BMW', 'X5', 2018, 'JKL1122', 'Available', 600.00, 'City Center'),
(5, 'Chevrolet', 'Malibu', 2020, 'MNO3344', 'Under Maintenance', 380.00, 'Downtown'),
(6, 'Tesla', 'Model 3', 2022, 'PQR5566', 'Available', 420.00, 'Suburbs'),
(7, 'Audi', 'A4', 2019, 'STU7788', 'Rented', 500.00, 'Airport'),
(8, 'Nissan', 'Altima', 2021, 'VWX9900', 'Available', 300.00, 'City Center');

-- Вставка данных в таблицу DimPayments
INSERT INTO DimPayments (Payment_ID, Payment_Method, Payment_Amount)
VALUES
(1, 'Credit Card', 350.00),
(2, 'Debit Card', 200.00),
(3, 'Cash', 450.00),
(4, 'Bank Transfer', 600.00),
(5, 'PayPal', 380.00),
(6, 'Apple Pay', 420.00),
(7, 'Google Pay', 500.00),
(8, 'Cryptocurrency', 300.00);

-- Вставка данных в таблицу DimTime
INSERT INTO DimTime (Date_ID, FullDate)
VALUES
(1, '2022-01-01'),
(2, '2024-02-01'),
(3, '2025-03-01'),
(4, '2025-04-01'),
(5, '2022-05-01'),
(6, '2025-06-01'),
(7, '2021-07-01'),
(8, '2025-08-01');

-- Вставка данных в таблицу FactOrders
INSERT INTO FactOrders (Order_ID, User_ID, Car_ID, Payment_ID, Date_ID, Start_Date, End_Date)
VALUES
(1, 3, 1, 1, 1, '2022-01-01', '2022-01-07'),
(2, 4, 2, 2, 2, '2024-02-01', '2024-02-05'),
(3, 5, 3, 3, 3, '2025-03-01', '2025-03-07'),
(4, 6, 4, 4, 4, '2025-04-01', '2025-04-10'),
(5, 7, 5, 5, 5, '2022-05-01', '2022-05-07'),
(6, 8, 6, 6, 6, '2025-06-01', '2025-06-03'),
(7, 3, 7, 7, 7, '2021-07-01', '2021-07-05'),
(8, 4, 8, 8, 8, '2025-08-01', '2025-08-10');
