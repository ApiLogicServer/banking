

DROP TABLE IF EXISTS AccountType;
CREATE TABLE AccountType (
  Name varchar(25) NOT NULL,
  PRIMARY KEY (Name)
) ;

INSERT INTO AccountType VALUES ('Checking'),('Loan'),('Savings');


DROP TABLE IF EXISTS Branch;
CREATE TABLE Branch (
  BranchID INTEGER PRIMARY KEY,
  Name varchar(100) DEFAULT NULL,
  Office varchar(15) DEFAULT NULL,
  Address varchar(100) DEFAULT NULL,
  OpenDate datetime DEFAULT NULL
) ;

INSERT INTO Branch VALUES (14,'Main','MainOffice','1 Main','2024-02-17 11:35:12'),(15,'Remote','RemoteOffice','Remoteville','2024-02-17 11:35:45');


DROP TABLE IF EXISTS Customer;
CREATE TABLE Customer (
  CustomerID INTEGER PRIMARY KEY,
  FirstName varchar(50) DEFAULT NULL,
  LastName varchar(50) DEFAULT NULL,
  Email varchar(100) DEFAULT NULL,
  PhoneNumber varchar(20) DEFAULT NULL,
  Address varchar(200) DEFAULT NULL,
  BirthDate date DEFAULT NULL,
  RegistrationDate datetime DEFAULT NULL,
  UserName varchar(64) NOT NULL,
  Password varchar(64) NOT NULL,
  BranchID int DEFAULT NULL,
  FOREIGN KEY (BranchID) REFERENCES Branch (BranchID)
) ;

INSERT INTO Customer VALUES (1,'Main','Customer',NULL,NULL,NULL,NULL,'2024-02-17 00:00:00','valued-customer','p',14),(2,'Remote','Customer',NULL,NULL,NULL,NULL,'2024-02-17 00:00:00','another-customer','p',15);


DROP TABLE IF EXISTS Account;
CREATE TABLE Account (
  AccountID INTEGER PRIMARY KEY,
  CustomerID int DEFAULT NULL,
  AccountType varchar(25) DEFAULT NULL,
  AcctBalance decimal(15,2) DEFAULT NULL,
  OpenDate datetime DEFAULT NULL,
  FOREIGN KEY (AccountType) REFERENCES AccountType (Name),
  FOREIGN KEY (CustomerID) REFERENCES Customer (CustomerID)
) ;

INSERT INTO `Account` VALUES (2,1,'Checking',200.00,'2024-02-17 12:51:47'),(4,1,'Savings',400.00,'2024-02-17 12:55:50');


DROP TABLE IF EXISTS Employees;
CREATE TABLE Employees (
  EmployeeID INTEGER  PRIMARY KEY,
  LastName varchar(15) NOT NULL,
  FirstName varchar(15) NOT NULL,
  Branch int DEFAULT '1',
  BirthDate datetime DEFAULT NULL,
  Photo varchar(25) DEFAULT NULL,
  Notes varchar(1024) DEFAULT NULL,
  FOREIGN KEY (Branch) REFERENCES Branch (BranchID)
) ;

INSERT INTO Employees VALUES (19,'Employee-Main','Joe',14,NULL,NULL,NULL),(20,'Employee-Remote','Mary',15,NULL,NULL,NULL);


DROP TABLE IF EXISTS TransactionLog;
CREATE TABLE TransactionLog (
  TransactionID INTEGER  PRIMARY KEY,
  AccountID int DEFAULT NULL,
  TransactionType varchar(25) DEFAULT NULL,
  TotalAmount decimal(15,2) DEFAULT NULL,
  Deposit decimal(15,2) DEFAULT NULL,
  Withdrawl decimal(15,2) DEFAULT NULL,
  ItemImage text,
  TransactionDate datetime DEFAULT NULL,
  FOREIGN KEY (AccountID) REFERENCES Account (AccountID)
) ;


DROP TABLE IF EXISTS Transfer;
CREATE TABLE Transfer (
  TransactionID INTEGER  PRIMARY KEY,
  FromAccountID int DEFAULT NULL,
  ToAccountID int DEFAULT NULL,
  Amount decimal(15,2) DEFAULT NULL,
  TransactionDate datetime DEFAULT NULL,

  FOREIGN KEY (FromAccountID) REFERENCES Account (AccountID),
  FOREIGN KEY (ToAccountID) REFERENCES Account (AccountID)
) ;

