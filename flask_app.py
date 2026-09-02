import os
from flask import Flask, render_template, request, redirect, flash, session, url_for
from bdd import inscription, verif_id, ajouter_commentaire, recuperer_commentaires
import sqlite3

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get("RETROGEN_SECRET_KEY", "dev-only-change-me")

@app.route('/')
def index():
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM produits WHERE id IN (1, 30, 14, 27)")
    produits = cursor.fetchall()
    connexion.close()
    
    return render_template('index.html', produits=produits)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/apropos')
def apropos():
    return render_template("apropos.html")

@app.route('/panier')
def panier():
    return render_template("panier.html")

####################  Boutique - Produits ####################

@app.route('/boutique')
def boutique():
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM produits")
    products = cursor.fetchall()
    connexion.close()

    return render_template("boutique.html", products=products)

@app.route('/produit/<int:product_id>')
def produit(product_id):
    connexion = sqlite3.connect('bdd.db')
    cursor = connexion.cursor()
    cursor.execute("SELECT * FROM produits WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    commentaires = recuperer_commentaires(product_id)
    connexion.close()
    if product:
        return render_template("produit.html", product=product, commentaires=commentaires)
    else:
        return "Produit non trouvé", 404

#################### Connexion et Inscription ####################

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", "rouge")
            return redirect('/register')

        if inscription(username, email, password):
            flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "vert")
            return redirect('/login')
        else:
            flash("Cet e-mail est déjà utilisé.", "rouge")
            return redirect('/register')

    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if verif_id(email, password):
            connexion = sqlite3.connect('bdd.db')
            cursor = connexion.cursor()
            cursor.execute("SELECT username FROM utilisateurs WHERE email = ?", (email,))
            user = cursor.fetchone()
            connexion.close()

            if user:
                session['username'] = user[0]
            session['email'] = email
            flash("Connexion établie avec succès !", "vert")
            return redirect('/')

        else:
            flash("Identifiant ou mot de passe incorrect.", "rouge")
            return redirect('/login')

    return render_template("login.html")

#################### Commentaires ####################

@app.route('/ajouter_commentaire/<int:produit_id>', methods=['POST'])
def ajouter_commentaire_route(produit_id):
    if 'username' not in session:
        flash("Vous devez être connecté pour laisser un commentaire.", "rouge")
        return redirect('/login')

    utilisateur = session['username']
    commentaire = request.form['commentaire']

    if 'note' not in request.form:
        flash("Veuillez noter le produit entre 1 et 5.", "rouge")
        return redirect(url_for('produit', product_id=produit_id))

    note = int(request.form['note'])

    if not (1 <= note <= 5):
        flash("La note doit être comprise entre 1 et 5.", "rouge")
        return redirect(url_for('produit', product_id=produit_id))

    ajouter_commentaire(produit_id, utilisateur, commentaire, note)
    flash("Votre commentaire a été ajouté avec succès !", "vert")

    return redirect(url_for('produit', product_id=produit_id))

#####################################################

if __name__ == '__main__':
    app.run(debug=True)
