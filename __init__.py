from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

  # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        # Vérifier les identifiants
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['authentifie'] = True
            # Rediriger vers la route lecture après une authentification réussie
            return redirect(url_for('lecture'))
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)


@app.route('/consultation2', methods=['GET'])
def consultation2():
    connection = sqlite3.connect('database2.db')
    cur = connection.cursor()
    cur.execute("SELECT * FROM Books")
    books = cur.fetchall()
    connection.close()
    return render_template('addordel.html', books=books)

@app.route('/consultation2/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    try:
        connection = sqlite3.connect('database2.db')
        cur = connection.cursor()
        cur.execute("DELETE FROM Books WHERE id = ?", (book_id,))
        connection.commit()
        connection.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/consultation2/add', methods=['POST'])
def add_book():
    try:
        title = request.form['title']
        author = request.form['author']
        isbn = request.form['isbn']
        stock = request.form['stock']
        connection = sqlite3.connect('database2.db')
        cur = connection.cursor()
        cur.execute("INSERT INTO Books (title, author, isbn, stock) VALUES (?, ?, ?, ?)",
                    (title, author, isbn, stock))
        connection.commit()
        book_id = cur.lastrowid
        connection.close()
        return jsonify({'success': True, 'book': {'id': book_id, 'title': title, 'author': author, 'isbn': isbn, 'stock': stock}})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/fiche_nom/', methods=['GET', 'POST'])
def search():
    data = None
    if request.method == 'POST':
        search_query = request.form['search']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, nom, prenom, adresse FROM clients WHERE nom LIKE ?', ('%' + search_query + '%',))
        data = cursor.fetchall()
        conn.close()
    return render_template('fiche_nom.html', data=data)

borrowed_books = []  

def get_db_connection():
    return sqlite3.connect('database2.db')

@app.route('/fiche_livre/', methods=['GET', 'POST'])
def searchbooks():
    books = None
    all_books = []  
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        search_query = request.form['search']
        cursor.execute('SELECT id, title, author, isbn, stock FROM Books WHERE title LIKE ?', ('%' + search_query + '%',))
        books = cursor.fetchall()
    else:
        cursor.execute('SELECT id, title, author, isbn, stock FROM Books')
        all_books = cursor.fetchall()

    conn.close()
    return render_template('fiche_livre.html', books=books, all_books=all_books, borrowed_books=borrowed_books)

@app.route('/emprunter/', methods=['POST'])
def emprunter():
    book_id = request.form['book_id']
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT id, title, author, isbn, stock FROM Books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    if book and book[4] > 0:  # Vérifier si le stock est disponible
        borrowed_books.append(book[:4])  # Ajouter aux emprunts sans stock
        cursor.execute('UPDATE Books SET stock = stock - 1 WHERE id = ?', (book_id,))
        conn.commit()

    conn.close()
    return redirect('/fiche_livre/')

@app.route('/rendre/', methods=['POST'])
def rendre():
    book_id = request.form['book_id']
    conn = get_db_connection()
    cursor = conn.cursor()
    borrowed_books[:] = [book for book in borrowed_books if str(book[0]) != book_id]
    cursor.execute('UPDATE Books SET stock = stock + 1 WHERE id = ?', (book_id,))
    conn.commit()
    
    conn.close()
    return redirect('/fiche_livre/')



@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement
                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)
