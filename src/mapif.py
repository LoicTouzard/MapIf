#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                       IMPORTS, GLOBALS AND MODULES INITIALIZATION
# ------------------------------------------------------------------------------------------

import hashlib
import binascii
import uuid
import os
import locale
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

# print current root for debugging
logger.mprint("Running from {0}".format(os.getcwd()))
# load config file and exit on error
logger.mprint("Loading configuration file...")
_APP_ROOT_=ini.getenv('OPENSHIFT_REPO_DIR', '')
if not ini.init_config(_APP_ROOT_+'mapif.ini'):
    logger.mprint("Configuration file is missing. Server can't be started !")
    exit(-1)

# initialize logging module
logger.mprint("Starting logging module...")
logger.init_logs()

# initialize DB module
logger.mprint("Starting DB module...")
db.init_db()

# set locale
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# create our little application :)
app = Flask(__name__)

# check Configuration section for more details
app.config.from_object(__name__)

# load secret key from configuration file or generated a UUID and use it as secret key
app.secret_key = ini.config('APP', 'secret_key', default=str(uuid.uuid4()))

# enable/disable debug
app.debug = ini.config('APP', 'debug', default=False, boolean=True)
if not app.debug:
    logger.mprint("Debugger is disabled !")
else:
    logger.mprint("Debugger is enabled.")

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
    return hashlib.sha256(bytearray(pwd_clear, encoding='utf8')).hexdigest()
    # unsupported Python 3.3 hash operation
    #dk = hashlib.pbkdf2_hmac('sha256', bytearray(pwd_clear, 'utf-8'), b'dev_salt', 100000)
    #return binascii.hexlify(dk).decode('utf-8')

def _internal_error(code):
    return json_response(
        Response(True, 
            "Une erreur interne au serveur s'est produite. Transmettez le CODE={0} suivant aux développeurs.".format(code)).json(), 
        status_code=500)

# ------------------------------------------------------------------------------------------
#                               FLASK ROUTES HANDLERS
# --------------------  ----------------------------------------------------------------------


@app.route('/', methods=['GET'])
def root():
    """
        This is the main application's route. It displays the application main page.
    """
    try:
        locations = db.get_locations_with_users()
        user_locations = None 
        if _check_connected(session):
            user_locations = db.get_user_locations(session['user']['id'])
        return render_template('layout.html', locations=locations, user_locations=user_locations) # users=users)
    except Exception as e:
        logger.log_error('mapif.root() error: details below.', e)
        return _internal_error('R00T_K0')


@app.route('/login', methods=['POST'])
def login():
    """
        This route is used to authenticate a user in the application
    """
    try:
        err = True
        content = "Opération interdite, vous êtes déjà connecté !"
        code = 403
        if not _check_connected(session):
            content = "L'utilisateur et/ou le mot de passe est érroné."
            code = 200
            email = request.form['email']
            pwd_clear = request.form['password']
            pwd_hash = _hash_pwd(pwd_clear)
            _load_user(session, email, pwd_hash)
            if _check_connected(session):
                err = False
                content = "Vous êtes maintenant connecté !"
        return json_response(Response(err, content).json(), status_code=code)
    except Exception as e:
        logger.log_error('mapif.login() error: details below.', e)
        return _internal_error('L0G1N_K0')
    
@app.route('/logout')
def logout():
    """
        This route is used to close the session of a connected user
    """
    try:
        err = True
        content = "Opération interdite, vous n'êtes pas connecté !"
        if not _check_connected(session):
            return json_response(Response(err, content).json(), status_code=403)
        else:
            session.pop('user', None)
        return redirect('/')
    except Exception as e:
        logger.log_error('mapif.logout() error: details below.', e)
        return _internal_error('L0G0U7_K0')

    
@app.route('/profil', methods=['POST'])
def profil():
    """
        This route will be used to update user profile
    """
    try:
        err = True
        content = "Opération interdite, vous n'êtes pas connecté !"
        if not _check_connected(session):
            return json_response(Response(err, content).json(), status_code=403)
        else:
            pass # TODO modification profil utilisateur
            return render_template('profil.html')
    except Exception as e:
        logger.log_error('mapif.profil() error: details below.', e)
        return _internal_error('PR0F1L_K0')
    
@app.route('/signup', methods=['POST'])
def signup():
    """
        This route is used by the application to add a new user to the application
    """
    try:
        err = True
        code = 403
        content = "Opération interdite, vous êtes déjà connecté !"
        if not _check_connected(session):
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
                pwd_hash = _hash_pwd(pwd_clear)
                # realisation si pas d'erreur
                if len(content.keys()) == 0:
                    content = "Cette adresse email est déjà attribuée à un utilisateur."
                    # verification de l'existence de l'utilisateur
                    if not db.user_exists(email):
                        # creation de l'utilisateur
                        db.create_user(firstname, lastname, email, pwd_hash, promo)
                        # chargement de l'utilisateur créé dans la session (connexion automatique après inscription)
                        _load_user(session, email, pwd_hash)
                        # mise à jour des variables de réponse 
                        err = False
                        content = 'ok'
        return json_response(Response(err, content).json(), status_code=code)
    except Exception as e:
        logger.log_error('mapif.signup() error: details below.', e)
        return _internal_error('S1NGUP_K0')


@app.route('/locations', methods=['GET'])
def locations():
    """
        This route is used to retrieve all locations for a given user 
    """
    try:
        err = True
        code = 200
        uid = request.args['uid']
        content = "Une erreur s'est produite, l'identifiant de l'utilisateur passé en paramètre n'est pas valide."
        if validator.validate(uid, 'int'):
            uid = int(uid)
            locations = db.get_user_locations(uid)
            content = "Une erreur s'est produite, aucune localisation n'a été trouvée pour cet utilisateur."
            if locations:
                err = False
                content = locations
        return json_response(Response(err, content).json(), status_code=code)
    except Exception as e:
        logger.log_error('mapif.locations() error: details below.', e)
        return _internal_error('L0C4T10N5_K0')


@app.route('/addlocation', methods=['POST'])
def addlocation():
    """
        This route is used to add a new location for a user
    """
    try:
        err = True
        content = "Opération interdite, vous n'êtes pas connecté !"
        code = 403
        if _check_connected(session):
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
    except Exception as e:
        logger.log_error('mapif.addlocation() error: details below.', e)
        return _internal_error('4DDL0C4T10N_K0')

@app.route('/delete', methods=['POST'])
def delete():
    """
        This route is used to delete completly a user account and all its data
    """
    try:
        err = True
        content = "Opération interdite vous n'êtes pas connecté !"
        code = 403
        if _check_connected(session):
            code = 200
            uid = session['user']['id']
            content = "La suppression du compte a échouée !"
            if db.delete_user(uid):
                err = False
                content = "Le compte a été supprimé avec succès."
        return json_response(Response(err, content).json(), status_code=code)
    except Exception as e:
        logger.log_error('mapif.delete() error: details below.', e)
        return _internal_error('D3L3T3_K0')

@app.errorhandler(404)
def page_not_found(e):
    """
        This is an error handler for 404 NOT FOUND exception
    """
    return render_template('404.html'), 404

# ------------------------------------------------------------------------------------------
#                               SERVER RUN FUNCTION
# ------------------------------------------------------------------------------------------
    
def run():
    """
        Start the application (dev only)
    """
    logger.mprint("Starting MapIf flask application...")
    app.run(host='localhost', port=5000)

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

def test():
    """
        Module unit tests
    """
    print('MAPIF - TESTS NOT IMPLEMENTED')
