#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                       IMPORTS, GLOBALS AND MODULES INITIALIZATION
# ------------------------------------------------------------------------------------------

import hashlib
import binascii
import uuid
from datetime import date
from flask import Flask 
from flask import request
from flask import session
from flask import redirect
from flask import abort
from flask import render_template
from flask import flash
from flask import escape
from flask.ext.responses import json_response
from flask.ext.responses import xml_response
from flask.ext.responses import auto_response
from flask.ext.cors import CORS
from src.utils import db
from src.utils.response import Response
from src.utils import validator
from src.utils import ini
from src.utils import logger

# load config file and exit on error
if not ini.init_config('mapif.ini'):
    print("Configuration file is missing. Server can't be started !")
    exit(-1)

# initialize logs
logger.init_logs()

# create our little application :)
app = Flask(__name__)

# check Configuration section for more details
app.config.from_object(__name__)

# load secret key from configuration file or generated a UUID and use it as secret key
app.secret_key = ini.config('APP', 'secret_key', default=str(uuid.uuid4()))

# allow cross origin requests on this application
CORS(app, resources={'/': {'origins': '*'}, '/': {'supports_credentials': True}})

# ------------------------------------------------------------------------------------------
#                               PRIVATE FUNCTIONS
# ------------------------------------------------------------------------------------------


def _load_user(session, email, pwd):
    usr = db.get_user(email, pwd)
    if usr:
        session['user'] = {
            'id': usr.id,
            'firstname': usr.firstname,
            'lastname': usr.lastname,
            'email': usr.email,
            'promo': usr.promo
        }


def _check_connected(session):
    return session.get('user', None)


def _hash_pwd(pwd_clear):
    dk = hashlib.pbkdf2_hmac('sha256', bytearray(pwd_clear, 'utf-8'), b'dev_salt', 100000)
    return binascii.hexlify(dk)

# ------------------------------------------------------------------------------------------
#                               FLASK ROUTES HANDLERS
# ------------------------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def root():
    #users = db.get_users_with_location()
    locations=db.get_locations_with_users()
    return render_template('map.html', locations=locations) # users=users)


@app.route('/login', methods=['POST'])
def login():
    err = True
    content = "Opération interdite, vous êtes déjà connecté !"
    code = 403
    if not check_connected(session):
        content = "L'utilisateur et/ou le mot de passe est érroné."
        code = 200
        email = request.form['email']
        pwd_clear = request.form['password']
        pwd_hash = hash_pwd(pwd_clear)
        load_user(session, email, pwd_hash)
        if check_connected(session):
            err = False
            content = "Vous êtes maintenant connecté !"
    return json_response(Response(err, content).json(), status_code=code)

    
@app.route('/logout')
def logout():
    err = True
    content = "Opération interdite, vous n'êtes pas connecté !"
    if not check_connected(session):
        return json_response(Response(err, content).json(), status_code=403)
    else:
        session.pop('user', None)
    return redirect('/')

    
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
    if not check_connected(session):
        code = 200
        content = "Captcha invalide. Annulation de l'inscription ! Encore un bot..."
        if validator.check_captcha(request):
            # recuperation du contenu de la requete
            firstname = escape(request.form['firstname'].strip())
            lastname = escape(request.form['lastname'].strip())
            email = request.form['email'].strip()
            pwd_clear = request.form['password1']
            pwd_clear2 = request.form['password2']
            promo = request.form['promo'].strip()
            # verification des champs
            content = {}
            if validator.is_empty(firstname):
                content['firstname'] = "Le champ prénom ne doit pas être vide !"
            if validator.is_empty(lastname):
                content['lastname'] = "Le champ nom ne doit pas être vide !"
            if not validator.validate(email, 'email'):
                content['email'] = "L'email ne respecte pas le format attendu !"
            if not validator.validate(promo, 'year') and int(promo) <= date.today().year:
                content['promo'] = "La promo n'est pas une année correctement formaté !"
            if len(pwd_clear) < 6:
                content['password1'] = "Le mot de passe doit faire au minimum 6 caractères !"
            if pwd_clear2 != pwd_clear:
                content['password2'] = "Les deux mots de passe doivent être identiques !"
            # hash password
            pwd_hash = hash_pwd(pwd_clear)
            # realisation si pas d'erreur
            if len(content.keys()) == 0:
                content = "Cette adresse email est déjà attribuée à un utilisateur."
                # verification de l'existence de l'utilisateur
                if not db.user_exists(email):
                    # creation de l'utilisateur
                    db.create_user(firstname, lastname, email, pwd_hash, promo)
                    # chargement de l'utilisateur créé dans la session (connexion automatique après inscription)
                    load_user(session, email, pwd_hash)
                    # mise à jour des variables de réponse 
                    err = False
                    content = 'ok'
    return json_response(Response(err, content).json(), status_code=code)


@app.route('/locations', methods=['GET'])
def locations():
    err = True
    code = 200
    uid = request.args['uid']
    content = "Une erreur s'est produite, l'identifiant de l'utilisateur passé en paramètre n'est pas valide."
    if validator.validate(uid, 'num'):
        uid = int(uid)
        locations = db.get_user_locations(uid)
        content = "Une erreur s'est produite, aucune localisation n'a été trouvée pour cet utilisateur."
        if locations:
            err = False
            content = locations
    return json_response(Response(err, content).json(), status_code=code)


@app.route('/addlocation', methods=['POST'])
def addlocation():
    err = True
    content = "Opération interdite, vous n'êtes pas connecté !"
    code = 403
    if check_connected(session):
        code = 200
        # recupération des données du post
        uid = session['user']['id']
        osm_id = escape(request.form['osm_id'].strip())
        osm_type = escape(request.form['osm_type'].strip())
        # vérification des champs
        content = {}
        if validator.is_empty(osm_id):
            content['osm_id'] = "Le champ osm_id ne doit pas être vide !"
        if validator.is_empty(osm_type):
            content['osm_type'] =  "Le champ osm_type ne doit pas être vide !"
        if len(content.keys()) == 0:
            # create user - location mapping record in db
            content = "L'ajout de la localisation a échoué. La localisation n'a pas été confirmée par Nominatim."
            if db.add_user_location(uid, osm_id, osm_type):
                # definition du message de retour
                err = False
                content = "La nouvelle localisation a été enregistrée."
    return json_response(Response(err, content).json(), status_code=code)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# ------------------------------------------------------------------------------------------
#                               SERVER RUN FUNCTION
# ------------------------------------------------------------------------------------------
    
def run():
    db.init_db()
    app.run(host='localhost', port=5000)

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

if __name__ == '__main__':
    print('NOTHING TO TEST HERE')