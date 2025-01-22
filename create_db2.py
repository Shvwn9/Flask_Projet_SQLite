import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('LibraryManagement.db')

# Chargement du schéma SQL
with open('schema2.sql') as f:
    connection.executescript(f.read())

# Création d'un curseur pour exécuter des requêtes SQL
cur = connection.cursor()

# Insertion des livres dans la table Books
cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)", 
            ('1984', 'George Orwell', '9780451524935', 5))
cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)", 
            ('To Kill a Mockingbird', 'Harper Lee', '9780061120084', 3))
cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)", 
            ('The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', 2))
cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)", 
            ('Pride and Prejudice', 'Jane Austen', '9780141439518', 4))
cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)", 
            ('Moby Dick', 'Herman Melville', '9781503280786', 6))
cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)", 
            ('War and Peace', 'Leo Tolstoy', '9781853260629', 3))
cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)", 
            ('The Catcher in the Rye', 'J.D. Salinger', '9780316769488', 5))
cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)", 
            ('The Hobbit', 'J.R.R. Tolkien', '9780547928227', 7))

# Validation des modifications
connection.commit()

# Fermeture de la connexion
connection.close()
