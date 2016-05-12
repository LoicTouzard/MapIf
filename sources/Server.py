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
from sources import db

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/users', methods=['GET'])
def users():
    users = db.get_all_users()
    return render_template('map.html', users=users)

@app.route('/login', methods=['POST'])
def login():
    status = None
    if request.method == 'POST':
        email = request.form['email']
        pwd = request.form['pwd']
        usr_id = db.get_user_id(email, pwd)
        if usr_id == -1:
            session['connected'] = False
            status = 'ko'
        else:
            session['connected'] = True
            status = 'ok'
    return jsonify(response={'status': status})
    
@app.route('/logout')
def logout():
    if session['connected']:
        session.pop('connected', None)
    return redirect(url_for('/'))
    
@app.route('/profil', methods=['GET', 'POST'])
def profil():
    if request.method == 'POST':
        pass # faire la modification de profil
    elif request.method == 'GET':
        return render_template('profil.html')
    
@app.route('/signup', methods=['POST'])
def inscrire():
    status = None
    if request.method == 'POST':
        firstname = request.form['firstname'];
        lastname = request.form['lastname']; 
        email = request.form['email']; 
        pwd = request.form['pwd']; 
        promo = request.form['promo'];
        db.create_user(firstname, lastname, email, pwd, promo)
        status = 'ok'
    else:
        status = 'ko'
    return flask.jsonify(response={'status': status})
    
# def connect_db():
    # return sqlite3.connect(app.config['DATABASE'])

# def init_db():
    # with closing(connect_db()) as db:
        # with app.open_resource('../schema.sql', mode='r') as f:
            # db.cursor().executescript(f.read())
        # db.commit()

# @app.before_request
# def before_request():
    # g.db = connect_db()

# @app.teardown_request
# def teardown_request(exception):
    # db = getattr(g, 'db', None)
    # if db is not None:
        # db.close()
        
def launch_server():
    db.init_db()
    app.run(host='0.0.0.0')
