-- Suppression des commandes CREATE DATABASE et USE
-- Créez directement les tables

-- Table Users
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('Admin', 'User')) DEFAULT 'User' NOT NULL
);

-- Table Books
CREATE TABLE IF NOT EXISTS Books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    stock INTEGER DEFAULT 0 NOT NULL
);

-- Table Borrowings
CREATE TABLE IF NOT EXISTS Borrowings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    borrow_date DATE NOT NULL,
    return_date DATE,
    status TEXT CHECK(status IN ('Borrowed', 'Returned')) DEFAULT 'Borrowed',
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (book_id) REFERENCES Books(id)
);

-- Table Recommendations (optionnelle)
CREATE TABLE IF NOT EXISTS Recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id INTEGER NOT NULL,
    recommended_books TEXT,
    FOREIGN KEY (book_id) REFERENCES Books(id)
);

-- Table Notifications (optionnelle)
CREATE TABLE IF NOT EXISTS Notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
