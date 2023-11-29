-- Inventory Table
CREATE TABLE Inventory (
    ISBN VARCHAR(20) PRIMARY KEY,
    Title VARCHAR(255),
    Author VARCHAR(255),
    Genre VARCHAR(50),
    Pages INT,
    ReleaseDate DATE,
    Stock INT
);

-- Cart Table
CREATE TABLE Cart (
    UserID INT,
    ISBN VARCHAR(20),
    Quantity INT,
    PRIMARY KEY (UserID, ISBN),
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (ISBN) REFERENCES Inventory(ISBN)
);

-- User Table
CREATE TABLE User (
    UserID INT PRIMARY KEY,
    Email VARCHAR(255),
    Password VARCHAR(255),
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    Address VARCHAR(255),
    City VARCHAR(100),
    State VARCHAR(50),
    Zip VARCHAR(20)
);
