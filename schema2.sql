-- Création de la base de données
CREATE DATABASE LibraryManagement;
USE LibraryManagement;

-- Table Users
CREATE TABLE Users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'User') DEFAULT 'User' NOT NULL
);

-- Table Books
CREATE TABLE Books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    stock INT DEFAULT 0 NOT NULL
);

-- Table Borrowings
CREATE TABLE Borrowings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE,
    status ENUM('Borrowed', 'Returned') DEFAULT 'Borrowed',
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (book_id) REFERENCES Books(id)
);

-- Table Recommendations (optionnelle)
CREATE TABLE Recommendations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    recommended_books TEXT,
    FOREIGN KEY (book_id) REFERENCES Books(id)
);

-- Table Notifications (optionnelle)
CREATE TABLE Notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

-- Insertion de données de test
INSERT INTO Users (name, email, password, role) VALUES
('Admin User', 'admin@library.com', 'adminpass', 'Admin'),
('John Doe', 'john.doe@example.com', 'userpass', 'User');

INSERT INTO Books (title, author, isbn, stock) VALUES
('1984', 'George Orwell', '9780451524935', 5),
('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 3),
('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 2);

-- Exemple d'emprunt
INSERT INTO Borrowings (user_id, book_id, borrow_date) VALUES
(2, 1, CURDATE());
