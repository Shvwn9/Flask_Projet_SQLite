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

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_admin() and not est_user():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification', next=request.path))
    elif est_admin():
        return "<h2>Bravo, vous êtes admin</h2>"
    elif est_user():
        return "<h2>Bravo, vous êtes user</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    next_url = request.args.get('next') or request.form.get('next') or url_for('lecture')
    print(f"Next URL: {next_url}")
    if request.method == 'POST':
        # Vérifier les identifiants admin
        if request.form['username'] == 'admin' and request.form['password'] == 'password': # password à cacher par la suite
            session['role'] = "admin"
            session['username'] = request.form['username']
            session['dernier_acces'] = time.time()  # Enregistrer le timestamp
            return redirect(next_url)
        # Vérifier les identifiants admin
        elif request.form['username'] == 'user' and request.form['password'] == '12345': # password à cacher par la suite
            session['role'] = "user"
            session['username'] = request.form['username']
            session['dernier_acces'] = time.time()  # Enregistrer le timestamp
            return redirect(next_url)
        else:
            # Afficher un message d'erreur si les identifiants sont incorrects 
            return render_template('formulaire_authentification.html', error=True, next=next_url)
    return render_template('formulaire_authentification.html', error=False, next=next_url)

# Déconnexion (pour tous les utilisateurs)
@app.route('/logout')
def logout():
    if not est_admin() and not est_user():
        return "<h2>Déjà déconnecté !</h2>"
    session.pop('role', None)
    session.pop('username', None)
    return "<h2>Déconnection, veuillez fermer la page !</h2>"

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

# Route pour afficher le formulaire de recherche
@app.route("/fiche_nom", methods=["GET"])
def formulaire_search():
    if est_admin() or est_user():
        return render_template("formulaire_search.html")
    print(request.path)
    return redirect(url_for('authentification', next=request.path))

# Route pour traiter la recherche
@app.route("/fiche_nom", methods=["POST"])
def search_client():
    nom = request.form["name"]

    # Connexion à la base de données
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Requête pour rechercher le nom
    cursor.execute("SELECT * FROM clients WHERE nom LIKE ? or prenom LIKE ?", ('%' + nom + '%','%' + nom + '%'))
    data = cursor.fetchall()
    conn.close()

    # Envoyer les résultats au template HTML
    return render_template("read_data.html", data=data)


#-----------------------------------------------------------------

#---------------------------SEQUENCE 6----------------------------

@app.route('/consultation2/')
def ReadBDD_livre():
    conn = sqlite3.connect('database2.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Books;')
    data = cursor.fetchall()
    conn.close()

    # Passer les données au template pour affichage
    return render_template('read_data2.html', data=data)

if __name__ == "__main__":
  app.run(debug=True)
