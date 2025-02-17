CREATE DATABASE Lab10;
USE Lab10;
GO
------------------------------------------------------------------------------------
EXEC sp_configure 'clr enabled', 1;
RECONFIGURE;
GO
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;
GO
EXEC sp_configure 'clr strict security', 0;
RECONFIGURE;
GO
------------------------------------------------------------------------------------
CREATE ASSEMBLY Lab10
FROM 'C:\Users\ascoltat0\Desktop\Lab10\Lab10\bin\Release\Lab10.dll'
WITH PERMISSION_SET = UNSAFE;  
GO
------------------------------------------------------------------------------------
CREATE TYPE dbo.PassportData EXTERNAL NAME Lab10.PassportData;
GO
------------------------------------------------------------------------------------
SELECT * FROM sys.assemblies;
SELECT * FROM sys.types WHERE name = 'PassportData';
------------------------------------------------------------------------------------
CREATE TABLE People (
    ID INT IDENTITY PRIMARY KEY,
    Name NVARCHAR(100),
    Passport PassportData
);
GO
INSERT INTO People (Name, Passport)
VALUES ('Дашуля Глухова', CONVERT(PassportData, 'AB 123456')),
       ('Лерка Рудяк', CONVERT(PassportData, 'CD 654321'));
GO
INSERT INTO People (Name, Passport)
VALUES ('Владислав Лемешевский', CONVERT(PassportData, 'AB123456'));
GO
SELECT ID, Name, Passport.ToString() AS [Passport] FROM People;
GO
------------------------------------------------------------------------------------
CREATE FUNCTION dbo.CalculateAverageWithoutMinMax (@values NVARCHAR(MAX))
RETURNS FLOAT
AS EXTERNAL NAME Lab10.UserDefinedFunctions.CalculateAverageWithoutMinMax;
GO
SELECT dbo.CalculateAverageWithoutMinMax('7, 2, 3, 4, 5, 6, 1') as [Avg];
GO
--DROP ASSEMBLY Lab10;
--DROP TYPE PassportData;
--DROP TABLE People;
--DROP FUNCTION dbo.CalculateAverageWithoutMinMax;SS