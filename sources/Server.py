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
from sources.utils import db
from sources.utils import response
from sources.utils import validator

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)

app = Flask(__name__)
# Check Configuration section for more details
app.config.from_object(__name__)
app.secret_key = 'development_'

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
    return jsonify(response=Response(err, content))
    
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
    status = None
    if request.method == 'POST':
        firstname = request.form['firstname'];
        lastname = request.form['lastname']; 
        email = request.form['email']; 
        pwd = request.form['password']; 
        promo = request.form['promo'];
        db.create_user(firstname, lastname, email, pwd, promo)
        load_user(session, email, pwd)
        status = 'ok'
    else:
        status = 'ko'
    return jsonify(response={'status': status})
    

def launch_server():
    db.init_db()
    app.run(host='0.0.0.0')
