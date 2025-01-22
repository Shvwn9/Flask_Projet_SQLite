from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session, g
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
import time  # Pour gérer le timestamp

app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

#------------------------SEQUENCE 5---------------------------

DB_FILE = "database.d"
DB_LIVRE = "database2.db"

# Durée maximale d'inactivité en secondes (10 minutes)
SESSION_TIMEOUT = 10 * 60

# Rendre la session disponible dans tous les templates
@app.context_processor
def inject_session():
    return dict(session=session)

# Fonction pour créer une clé "authentifie" dans la session utilisateur
# Vérification des rôles dans la session 
def est_admin():
    return session.get('role') == 'admin'

def est_user():
    return session.get('role') == 'user'

# Vérification du timeout avant chaque requête
@app.before_request
def verifier_inactivite():
    # Vérifier si l'utilisateur est connecté
    if 'role' in session:
        dernier_acces = session.get('dernier_acces', None)
        maintenant = time.time()
        
        # Si le dernier accès est défini et dépasse le timeout
        if dernier_acces and (maintenant - dernier_acces > SESSION_TIMEOUT):
            # Supprimer la session et rediriger vers la déconnexion
            session.clear()
            return redirect(url_for('logout'))
        
        # Mettre à jour le timestamp du dernier accès
        session['dernier_acces'] = maintenant
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


@app.route('/consultation2/')
def ReadBDD_livre():
    conn = sqlite3.connect('database2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data2.html', data=data)




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
