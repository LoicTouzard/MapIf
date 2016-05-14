# all the imports
import sqlite3
from contextlib import closing
from flask import Flask 
from flask import request
from flask import session
from flask import redirect
from flask import url_for
from flask import abort
from flask import render_template
from flask import flash
from flask import escape
from flask.ext.responses import json_response
from flask.ext.responses import xml_response
from flask.ext.responses import auto_response
from sources.utils import db
from sources.utils.response import Response
from sources.utils import validator
from datetime import date
import hashlib
import binascii

# configuration
DEBUG = True
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)

app = Flask(__name__)
# Check Configuration section for more details
app.config.from_object(__name__)
app.secret_key = 'development_key'

# --------------------------
#   Fonction utilitaires
# --------------------------

def load_user(session, email, pwd):
    usr = db.get_user(email, pwd)
    if usr:
        session['user'] = {
            'id': usr.id,
            'firstname': usr.firstname,
            'lastname': usr.lastname,
            'email': usr.email,
            'promo': usr.promo
        }


def check_connected(session):
    return session.get('user', None)

# --------------------------
#   Handlers de l'API
# --------------------------

@app.route('/', methods=['GET'])
def root():
    users = db.get_all_users()
    return render_template('map.html', users=users)

@app.route('/login', methods=['POST'])
def login():
    err = True
    content = "Opération interdite, vous êtes déjà connecté !"
    code = 403
    if not check_connected(session):
        content = "L'utilisateur et/ou le mot de passe est érroné."
        code = 200
        if request.method == 'POST':
            email = request.form['email']
            pwd = request.form['pwd']
            load_user(session, email, pwd)
            if session['user']:
                err = False
                content = 'ok'
    return json_response(Response(err, content).json(), status_code=code)
    
@app.route('/logout')
def logout():
    err = True
    content = "Opération interdite, vous n'êtes pas connecté !"
    if not check_connected(session):
        return json_response(Response(err, content).json(), status_code=403)
    else:
        session.pop('user', None)
    return redirect(url_for('/'))
    
@app.route('/profil', methods=['POST'])
def profil():
    err = True
    content = "Opération interdite, vous n'êtes pas connecté !"
    if not check_connected(session):
        return json_response(Response(err, content).json(), status_code=403)
    else:
        pass # TODO modification profil utilisateur
        return render_template('profil.html')
    
@app.route('/signup', methods=['POST'])
def signup():
    err = True
    code = 403
    content = "Opération interdite, vous êtes déjà connecté !"
    if check_connected(session):
        code = 200
        content = "Une erreur s'est produite, l'inscription de l'utilisateur est annulée."
        # recuperation du contenu de la requete
        firstname = escape(request.form['firstname'])
        lastname = escape(request.form['lastname'])
        email = request.form['email']
        pwd_clear = request.form['password']
        dk = hashlib.pbkdf2_hmac('sha256', pwd_clear, b'dev_salt')
        pwd_hash = binascii.hexlify(dk)
        promo = request.form['promo']
        # verification des champs
        if not validator.validate(email, 'email'):
            content = "L'email ne respecte pas le format attendu !"
        elif not validator.validate(promo, 'year') and int(promo) <= date.today().year:
            content = "La promo n'est pas une année correctement formaté"
        else:
            # creation de l'utilisateur
            db.create_user(firstname, lastname, email, pwd, promo)
            # chargement de l'utilisateur créé dans la session (connexion automatique après inscription)
            load_user(session, email, pwd)
            # mise à jour des variables de réponse 
            err = False
            content = 'ok'
    return json_response(Response(err, content).json(), status_code=code)

@app.route('/locations', methods=['POST'])
def locations():
    err = True
    content = "Opération interdite, vous êtes déjà connecté !"
    code = 403
    if check_connected(session):
        code = 200
        uid = request.form['uid']
        content = "Une erreur s'est produite, l'identifiant de l'utilisateur passé en paramètre n'est pas valide."
        if validator.validate(uid, 'num'):
            uid = int(uid)
            locations = get_user_locations(uid)
            content = "Une erreur s'est produite, aucune localisation n'a été trouvée pour cet utilisateur."
            if locations:
                err = False
                content = locations
    return json_response(Response(err, content).json(), status_code=code)

# -----------------------
#   Lancement du serveur
# -----------------------

def launch_server():
    db.init_db()
    app.run(host='0.0.0.0')
