import hashlib
import sqlite3
import datetime
from produits import produits

def create_if_not_exist():
    """ Crée les tables utilisateurs, produits et commentaires si elles n'existent pas """
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS utilisateurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            mot_de_passe TEXT NOT NULL
        )
    ''')
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            categorie TEXT NOT NULL,
            prix REAL NOT NULL,
            description TEXT NOT NULL,
            image_url TEXT
        )
    ''')
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS commentaires (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produit_id INTEGER NOT NULL,
            commentaire TEXT NOT NULL,
            note INTEGER,
            date TEXT,
            utilisateur TEXT,  -- Ajoute la colonne utilisateur
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        )
    ''')
    connexion.commit()
    connexion.close()

#################### Fonctions pour Ajouter des Produits ####################

def ajouter_produit(nom, categorie, prix, description, image_url):
    """ Ajoute un produit dans la base de données """
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute(''' 
        INSERT INTO produits (nom, categorie, prix, description, image_url) 
        VALUES (?, ?, ?, ?, ?)
    ''', (nom, categorie, prix, description, image_url))
    connexion.commit()
    connexion.close()

def inserer_produits_si_vide():
    """ Ajoute des produits si la table est vide """
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM produits")
    if cursor.fetchone()[0] == 0:
        for produit in produits:
            cursor.execute(''' 
                INSERT INTO produits (nom, categorie, prix, description, image_url) 
                VALUES (?, ?, ?, ?, ?)
            ''', (produit[0], produit[1], produit[2], produit[3], produit[4]))
        connexion.commit()

    connexion.close()

#################### Commentaires ####################

def ajouter_commentaire(produit_id, utilisateur, commentaire, note):
    """ Ajoute un commentaire à la base de données """
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    date_ajout = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(''' 
        INSERT INTO commentaires (produit_id, utilisateur, commentaire, note, date) 
        VALUES (?, ?, ?, ?, ?)
    ''', (produit_id, utilisateur, commentaire, note, date_ajout))
    connexion.commit()
    connexion.close()

def recuperer_commentaires(produit_id):
    """ Récupère tous les commentaires pour un produit donné """
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute(''' 
        SELECT c.commentaire, c.note, c.utilisateur, c.date
        FROM commentaires c
        WHERE c.produit_id = ?
        ORDER BY c.date DESC
    ''', (produit_id,))
    commentaires = cursor.fetchall()
    connexion.close()
    return commentaires

#################### Inscription - Connexion ####################

def hash_password(mot_de_passe):
    """ Fonction pour hacher le mot de passe avec SHA256 """
    return hashlib.sha256(mot_de_passe.encode('utf-8')).hexdigest()

def inscription(username, email, mot_de_passe):
    """ Crée un utilisateur avec un mot de passe haché """
    hashed_password = hash_password(mot_de_passe)

    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute('SELECT email FROM utilisateurs WHERE email = ?', (email,))
    if cursor.fetchone():
        connexion.close()
        return False
    cursor.execute(''' 
        INSERT INTO utilisateurs (username, email, mot_de_passe) 
        VALUES (?, ?, ?)
    ''', (username, email, hashed_password))
    connexion.commit()
    connexion.close()
    return True

def verif_id(email, mot_de_passe):
    """ Vérifie si l'utilisateur existe et si le mot de passe est correct """
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute('''SELECT mot_de_passe FROM utilisateurs WHERE email = ?''', (email,))
    user = cursor.fetchone()
    connexion.close()

    if user:
        return user[0] == hash_password(mot_de_passe)
    return False

#################### Récupérer les Produits ####################

def recuperer_produits():
    """ Récupère tous les produits de la base de données """
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM produits")
    produits = cursor.fetchall()
    connexion.close()
    return produits if produits else []

def recuperer_produit_par_id(produit_id):
    """ Récupère un produit par son ID """
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM produits WHERE id = ?", (produit_id,))
    produit = cursor.fetchone()
    connexion.close()
    return produit

########################################################

create_if_not_exist()
inserer_produits_si_vide()