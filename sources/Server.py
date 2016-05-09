# all the imports
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from sources import User
from sources import db

# configuration
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def list():
    cur = g.db.execute('select nom, prenom, lat, lon from users')
    users = []
    for row in cur.fetchall():
        u = User.User(row[0],row[1],None,'nico',None,None)
        u.setLatLon(row[2],row[3])
        users.append(u)
    return render_template('list.html', users=users)
    
@app.route('/map')
def map():
    cur = g.db.execute('select nom, prenom, lat, lon from users')
    users = []
    for row in cur.fetchall():
        u = User.User(row[0],row[1],None,'nico',None,None)
        u.setLatLon(row[2],row[3])
        users.append(u)
    return render_template('map.html', users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        login = request.form['username']
        mdp = request.form['password']
        cur = g.db.execute('select id from users where email = ? and mdp = ?',(login,mdp,))
        if(cur.fetchone() is None):
            error = "Problème durant l'authentification !"
        else:
            session['logged_in'] = request.form['username']
            return redirect(url_for('list'))
    return render_template('login.html',error=error)
    
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('list'))
    
@app.route('/profil', methods=['GET', 'POST'])
def profil():
    if request.method == 'POST':
        pass # faire la modification de profil
    elif request.method == 'GET':
        return render_template('profil.html')
    
@app.route('/inscrire')
def inscrire():
    error = None
    db.update_user("Jean", "VALJEAN", "jean.valjan@plouc.com", "password", "1854")
    return render_template('signup.html',error=error)
    
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
    