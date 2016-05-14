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
from flask import jsonify
from flask import escape
from sources.utils import db
from sources.utils.response import Response
from sources.utils import validator
from datetime import date

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
            'firstname': usr.firstname,
            'lastname': usr.lastname,
            'email': usr.email,
            'promo': usr.promo
        }

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
    content = "L'utilisateur et/ou le mot de passe est érroné."
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        load_user(session, email, pwd)
        if session['user']:
            err = False
            content = 'ok'
    return jsonify(response=Response(err, content).json())
    
@app.route('/logout')
def logout():
    if session['user']:
        session.pop('user', None)
    return redirect(url_for('/'))
    
@app.route('/profil', methods=['GET', 'POST'])
def profil():
    if request.method == 'POST':
        pass # faire la modification de profil
    elif request.method == 'GET':
        return render_template('profil.html')
    
@app.route('/signup', methods=['POST'])
def signup():
    err = True
    content = "Une erreur s'est produite, l'inscription de l'utilisateur est annulée."
    if request.method == 'POST':
        firstname = escape(request.form['firstname'])
        lastname = escape(request.form['lastname'])
        email = request.form['email']
        pwd = request.form['password'] 
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
    return jsonify(response=Response(err, content).json())
    

def launch_server():
    db.init_db()
    app.run(host='0.0.0.0')
