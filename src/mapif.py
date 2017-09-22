#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: mapif.py
#    date: 2017-09-22
# authors: loic.touzard, david.wobrock, paul.dautry, ...
# purpose:
#       MapIF Flask application 
# license:
#    MapIF - Where are INSA de Lyon IF students right now ?
#    Copyright (C) 2017  Loic Touzard
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#===============================================================================
# IMPORTS
#===============================================================================
import hashlib
import binascii
import uuid
import os
import locale
import datetime
from flask import Flask
from flask import request
from flask import session
from flask import redirect
from flask import abort
from flask import render_template
from flask import flash
from flask import escape
from flask_responses import json_response
from flask_responses import xml_response
from flask_responses import auto_response
from flask_cors import CORS
from src.utils import db
from src.utils.response import Response
from src.utils import validator
from src.utils import ini
from src.utils import logger
from src.utils import emails
from src.utils.wrappers import internal_error_handler
from src.utils.wrappers import require_connected
from src.utils.wrappers import require_disconnected
#===============================================================================
# GLOBALS
#===============================================================================
# print current root for debugging
logger.mprint("Running from {0}".format(os.getcwd()))
# load config file and exit on error
logger.mprint("Loading configuration file...")
if not ini.init_config('mapif.ini'):
    logger.mprint("Configuration file is missing. Server can't be started !")
    exit(-1)
# initialize logging module
logger.mprint("Starting logging module...")
logger.init_logs()
# initialize DB module
logger.mprint("Starting DB module...")
db.init_db()
# initialise emails module
emails.init_emails()
# set locale
locale.setlocale(locale.LC_ALL, ini.config('APP', 'locale', default='fr_FR.UTF-8'))
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
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# _load_user
#   set user in session
#-------------------------------------------------------------------------------
def _load_user(session, email, sha_pwd):
    usr = db.get_user(email, sha_pwd)
    if usr:
        session['user'] = {
            'id': usr.id,
            'firstname': usr.firstname,
            'lastname': usr.lastname,
            'email': usr.email,
            'promo': usr.promo
        }
#-------------------------------------------------------------------------------
# _update_user
#   update user information in session
#-------------------------------------------------------------------------------
def _update_user(session, uid):
    usr = db.get_user_by_id(uid)
    if usr:
        session['user'] = {
            'id': usr.id,
            'firstname': usr.firstname,
            'lastname': usr.lastname,
            'email': usr.email,
            'promo': usr.promo
        }
#-------------------------------------------------------------------------------
# _check_connected
#   check if user is connected (user in session)
#-------------------------------------------------------------------------------
def _check_connected(session):
    return session.get('user', None)
#-------------------------------------------------------------------------------
# _hash_pwd
#   hash given password using SHA-256 algorithm from hashlib
#-------------------------------------------------------------------------------
def _hash_pwd(pwd_clear):
    return hashlib.sha256(pwd_clear.encode()).hexdigest()
#===============================================================================
# FLASK ROUTES
#===============================================================================
#-------------------------------------------------------------------------------
# beforeRequest
#   override of Flask.beforeRequest method to ensure client is using HTTPS !
#-------------------------------------------------------------------------------
@app.before_request
def beforeRequest():
    if not app.debug and 'https' not in request.url:
        return redirect(request.url.replace('http', 'https'))
#-------------------------------------------------------------------------------
# root
#   This is the main application's route. It displays the application main page.
#-------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@internal_error_handler('R00TK0')
def root():
    locations = db.get_locations_with_users()
    user_locations = None
    if _check_connected(session):
        user_locations = db.get_user_locations(session['user']['id'])
    return render_template('map.html', locations=locations, user_locations=user_locations, active="map") # users=users)
#-------------------------------------------------------------------------------
# profile
#   This is profile view of the current user.
#-------------------------------------------------------------------------------
@app.route('/profil', methods=['GET'])
@internal_error_handler('PR0F1LK0')
@require_connected()
def profile():
    user_locations = db.get_user_locations(session['user']['id'])
    return render_template('profile.html', user_locations=user_locations, active='profile') # users=users)
#-------------------------------------------------------------------------------
# login
#   This route is used to authenticate a user in the application
#-------------------------------------------------------------------------------
@app.route('/login', methods=['POST'])
@internal_error_handler('L0G1NK0')
@require_disconnected()
def login():
    content = "L'utilisateur et/ou le mot de passe est érroné."
    email = request.form['email']
    pwd_clear = request.form['password']
    pwd_hash = _hash_pwd(pwd_clear)
    _load_user(session, email, pwd_hash)
    err = True
    if _check_connected(session):
        err = False
        content = "Vous êtes maintenant connecté !"
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# logout
#   This route is used to close the session of a connected user
#-------------------------------------------------------------------------------
@app.route('/logout')
@internal_error_handler('L0G0U7K0')
@require_connected()
def logout():
    session.pop('user', None)
    return redirect('/')
#-------------------------------------------------------------------------------
# password_reset
#   This route can be used to generate a token for the given user, and send it 
#   to him via email
#-------------------------------------------------------------------------------
@app.route('/password', methods=['POST'])
@internal_error_handler('PA55W0RDK0')
@require_disconnected()
def password_reset():
    email = request.form['email']
    logger.mprint('Asking for password reset for: {0}'.format(email))
    if not db.user_exists(email):
        error = True
        content = "Cette adresse électronique n'est associée à aucun utilisateur."
        logger.mprint('{0} does not exist'.format(email))
        return json_response(Response(error, content).json(), status_code=200)
    token = db.create_or_update_password_reset(email, app.secret_key)
    logger.mprint("Created/updated user's password reset object with token '{0}'".format(token))
    reset_link = "{0}password-reset?token={1}&email={2}".format(request.url_root, token, email)
    user = db.get_user_by_email(email)
    emails.send_password_reset_mail(email, user.firstname, token)
    logger.mprint("Process finished sending mail to {0} with link '{1}'".format(email, reset_link))
    error = False
    content = "Un lien pour modifier ton mot de passe a été envoyé à cette adresse, il expirera dans 10 minutes."
    return json_response(Response(error, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# password_reset_page
#   
#-------------------------------------------------------------------------------
@app.route('/password-reset', methods=['GET', 'POST'])
@internal_error_handler('PA55W0RDK0R3S3T')
@require_disconnected()
def password_reset_page():
    # Get parameters: email + token (must both be setted)
    if 'token' not in request.args or 'email' not in request.args:
        logger.mprint("Leaving password reset: no 'token' and 'email'")
        return page_not_found(None)
    token = request.args['token']
    email = request.args['email']
    # Find if user exists (must exist)
    if not db.user_exists(email):
        logger.mprint("Leaving password reset: user does not exist")
        return page_not_found(None)
    user = db.get_user_by_email(email)
    # Find PasswordReset instance from this user with this token exists (must exist)
    password_reset = db.get_password_reset_by_token_and_uid(token, user.id)
    if password_reset is None:
        logger.mprint("Leaving password reset: PasswordReset instance doesn't exist")
        return page_not_found(None)
    # Test if PasswordReset intance is not used (must not be used)
    if password_reset.used is True:
        logger.mprint("Leaving password reset: PasswordReset instance has been used already")
        return page_not_found(None)
    # Test if PasswordReset instance if not too old
    reset_timestamp = password_reset.timestamp
    now_timestamp = datetime.datetime.now()
    delay_minutes = 10
    if (now_timestamp - reset_timestamp) > datetime.timedelta(minutes=delay_minutes):
        logger.mprint("Leaving password reset: PasswordReset instance is too old ({0} and now is {1})".format(reset_timestamp, now_timestamp))
        return page_not_found("Autorisation expirée (plus de {0} minutes). Redemandes une nouvelle autorisation.".format(delay_minutes))
    # If method is GET, return template
    if request.method == 'GET':
        logger.mprint("Getting password reset page")
        return render_template('password-reset.html', reset_form=True)
    # Else if POST, update password of user
    elif request.method == 'POST':
        logger.mprint("Updating password")
        if 'password1' not in request.form or 'password2' not in request.form or request.form['password1'] != request.form['password2']:
            return render_template('password-reset.html', reset_form=True, error='Deux fois le même mot de passe on a dit...')
        new_pass = request.form['password1']
        hashed_pass = _hash_pwd(new_pass)
        if db.update_user(user.id, pwd=hashed_pass):
            db.set_password_reset_used(password_reset)
            return render_template('password-reset.html', reset_form=False)
        else:
            return render_template('password-reset.html', reset_form=True, error='A merde, y a eu une couille.')
#-------------------------------------------------------------------------------
# search_users
#   This route can be used to search users based on given filters
#-------------------------------------------------------------------------------
@app.route('/search/users', methods=['POST'])
@internal_error_handler('534RCHU53R5K0')
@require_connected()
def search_users():
    filters = request.form['filters']
    content = db.get_users(filters)
    return json_response(Response(False, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# account_create
#   This route can be used by the application to add a new user to the application
#-------------------------------------------------------------------------------
@app.route('/account/create', methods=['POST'])
@internal_error_handler('4CC0U7CR34T3K0')
@require_disconnected()
def account_create():
    content = "Captcha invalide. Annulation de l'inscription ! Encore un bot..."
    err = True
    if app.debug or validator.check_captcha(request):
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
        if not validator.validate(promo, 'year'):
            content['promo'] = "La promo n'est pas une année correctement formaté !"
        if int(promo) < 1969 or int(promo) >= (datetime.datetime.now().year+4):
            content['promo'] = "L'année est en dehors de l'intervalle autorisé !"
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
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# account_update_names
#   This route can be used to update user profile firstname and lastname
#-------------------------------------------------------------------------------
@app.route('/account/update/names', methods=['PATCH'])
@internal_error_handler('4CC0U7UPD4T3NAM35K0')
@require_connected()
def account_update_names():
    err = True
    firstname = escape(request.form['firstname'].strip())
    lastname = escape(request.form['lastname'].strip())
    # verification des champs
    content = {}
    if validator.is_empty(firstname):
        content['firstname'] = "Le champ prénom ne doit pas être vide !"
    if validator.is_empty(lastname):
        content['lastname'] = "Le champ nom ne doit pas être vide !"
    # realisation si pas d'erreur
    if len(content.keys()) == 0:
        content = "La mise à jour du profil a échouée"
        # verification de l'existence de l'utilisateur
        if db.update_user(session['user']['id'], firstname=firstname, lastname=lastname):
            _update_user(session, session['user']['id'])
            # mise à jour des variables de réponse 
            err = False
            content = 'ok'
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# account_update_email
#   This route can be used to update user email
#-------------------------------------------------------------------------------
@app.route('/account/update/email', methods=['PATCH'])
@internal_error_handler('4CC0U7UPD4T33MA1LK0')
@require_connected()
def account_update_email():
    err = True
    email = request.form['email'].strip()
    # verification des champs
    content = {}
    if not validator.validate(email, 'email'):
        content['email'] = "L'email ne respecte pas le format attendu !"
    # realisation si pas d'erreur
    if len(content.keys()) == 0:
        content['email'] = "Cette adresse email est déjà attribuée à un utilisateur."
        # verification de l'existence de l'utilisateur
        if not db.user_exists(email):
            content = "La mise à jour du profil a échouée"
            # verification de l'existence de l'utilisateur
            if db.update_user(session['user']['id'], email=email):
                _update_user(session, session['user']['id'])
                # mise à jour des variables de réponse 
                err = False
                content = 'ok'
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# account_update_password
#   This route can be used to update user password
#-------------------------------------------------------------------------------
@app.route('/account/update/password', methods=['PATCH'])
@internal_error_handler('4CC0U7UPD4T3PA55W0RDK0')
@require_connected()
def account_update_password():
    err = True
    pwd_old = request.form['password_old']
    pwd_clear = request.form['password1']
    pwd_clear2 = request.form['password2']
    # verification des champs
    content = {}
    # if pwd_old != ancien mdp
    if db.check_user_password(session['user']['id'], _hash_pwd(pwd_old)):
        content['password_old'] = "Le mot de passe est incorrect !"
    if len(pwd_clear) < 6:
        content['password1'] = "Le mot de passe doit faire au minimum 6 caractères !"
    if pwd_clear2 != pwd_clear:
        content['password2'] = "Les deux mots de passe doivent être identiques !"
    # hash password
    pwd_hash = _hash_pwd(pwd_clear)
    # realisation si pas d'erreur
    if len(content.keys()) == 0:
        content = "La mise à jour du profil a échouée"
        # verification de l'existence de l'utilisateur
        if db.update_user(session['user']['id'], pwd=pwd_hash):
            # _update_user(session, session['user']['id'])
            # mise à jour des variables de réponse 
            err = False
            content = 'ok'
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# account_update_promo
#   This route can be used to update user promotion
#-------------------------------------------------------------------------------
@app.route('/account/update/promo', methods=['PATCH'])
@internal_error_handler('4CC0U7UPD4T3PR0M0K0')
@require_connected()
def account_update_promo():
    err = True
    promo = request.form['promo'].strip()
    # verification des champs
    content = {}
    if not validator.validate(promo, 'year'):
        content['promo'] = "La promo n'est pas une année correctement formaté !"
    if int(promo) < 1969 or int(promo) >= (datetime.datetime.now().year+4):
        content['promo'] = "L'année est en dehors de l'intervalle autorisé !"
    # realisation si pas d'erreur
    if len(content.keys()) == 0:
        content = "La mise à jour du profil a échouée"
        # verification de l'existence de l'utilisateur
        if db.update_user(session['user']['id'], promo=promo):
            _update_user(session, session['user']['id'])
            # mise à jour des variables de réponse 
            err = False
            content = 'ok'
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# account_delete
#   This route can be used to delete completly a user account and all its data
#-------------------------------------------------------------------------------
@app.route('/account/delete', methods=['DELETE'])
@internal_error_handler('4CC0UN7D3L3T3K0')
@require_connected()
def account_delete():
    uid = session['user']['id']
    db.delete_user(uid)
    session.pop('user', None)
    err = False
    content = "Le compte a été supprimé avec succès."
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# locations
#   This route can be used to retrieve all locations for a given user 
#-------------------------------------------------------------------------------
@app.route('/locations', methods=['POST'])
@internal_error_handler('L0C4T10N5K0')
def locations():
    err = True
    code = 200
    uid = request.form['uid']
    content = "Une erreur s'est produite, l'identifiant de l'utilisateur passé en paramètre n'est pas valide."
    if not validator.validate(uid, 'int'):
        uid = int(uid)
        locations = db.get_user_locations(uid)
        content = "Une erreur s'est produite, aucune localisation n'a été trouvée pour cet utilisateur."
        if locations:
            err = False
            content = locations
    return json_response(Response(err, content).json(), status_code=code)
#-------------------------------------------------------------------------------
# location_create
#   This route can be used to add a new location for a user
#-------------------------------------------------------------------------------
@app.route('/user/location/create', methods=['POST'])
@internal_error_handler('L0C4T10N4DDK0')
@require_connected()
def location_create():
    # recupération des données du post
    uid = session['user']['id']
    osm_id = escape(request.form['osm_id'].strip())
    osm_type = escape(request.form['osm_type'].strip())
    # construction du bloc de metadonnées
    metadata = {}
    metadata['reason'] = escape(request.form['reason'].strip())
    # vérification des champs
    content = {}
    err = True
    if not validator.validate(osm_id, 'int'):
        content['osm_id'] = "Le champ osm_id doit être un identifiant numérique !"
    if validator.is_empty(osm_type):
        content['osm_type'] =  "Le champ osm_type ne doit pas être vide !"
    if metadata['reason'] not in ['no', 'internship', 'exchange', 'dd', 'job', 'vacation']:
        content['meta']['reason'] = "La valeur de la métadonnée raison est invalide."
    if len(content.keys()) == 0:
        # create user - location mapping record in db
        content = "L'ajout de la localisation a échoué. La localisation n'a pas été confirmée par Nominatim."
        if db.create_user_location(uid, osm_id, osm_type, metadata):
            err = False
            content = "La nouvelle localisation a été enregistrée."
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# location_update
#   This route can be used to update a user location
#-------------------------------------------------------------------------------
@app.route('/user/location/update', methods=['POST'])
@internal_error_handler('L0C4T10NUPD4T3K0')
@require_connected()
def location_update():
    # recupération des données du post
    uid = session['user']['id']
    osm_id = escape(request.form['osm_id'].strip())
    timestamp = escape(request.form['timestamp'].strip())
    # vérification des champs
    content = {}
    err = True
    if not validator.validate(osm_id, 'int'):
        content['osm_id'] = "L'osm_id transmis ne respecte pas le format attendu: nombre entier."
    if not validator.validate(timestamp, 'timestamp'):
        content['timestamp'] =  "Le timestamp ne respecte pas le format attendu: YYYY-mm-dd"
    if len(content.keys()) == 0:
        # update timestamp
        content = "La mise à jour de la localisation est un échec. Une erreur de persistence s'est produite."
        if db.update_user_location(uid, osm_id, timestamp):
            err = False
            content = "La localisation a été mise à jour."
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# location_delete
#   This route can be used to delete a user location
#-------------------------------------------------------------------------------
@app.route('/user/location/delete', methods=['DELETE'])
@internal_error_handler('L0C4T10ND3L3T3K0')
def location_delete():
    # recupération des données du post
    uid = session['user']['id']
    osm_id = escape(request.form['osm_id'].strip())
    timestamp = escape(request.form['timestamp'].strip())
    # vérification des champs
    content = {}
    err = True
    if not validator.validate(osm_id, 'int'):
        content['osm_id'] = "L'osm_id transmis ne respecte pas le format attendu: nombre entier."
    if not validator.validate(timestamp, 'timestamp'):
        content['timestamp'] =  "Le timestamp ne respecte pas le format attendu: YYYY-mm-dd"
    if len(content.keys()) == 0:
        # delete location 
        content = "La suppression de la localisation n'a pas aboutie !"
        if db.delete_user_location(uid, osm_id, timestamp):
            err = False
            content = "La localisation a été supprimée de votre historique."
    return json_response(Response(err, content).json(), status_code=200)
#-------------------------------------------------------------------------------
# page_not_found
#   This is an error handler for 404 NOT FOUND exception
#-------------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(msg):
    return render_template('404.html', message=msg), 404
#===============================================================================
# SERVER FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# run
#   Start the application (dev only, production should use uWSGI with wsgi.py)
#-------------------------------------------------------------------------------
def run():
    port = 5000
    logger.mprint("Starting MapIf flask application...")
    logger.mprint("Launching server on localhost, port {0}".format(port))
    app.run(host='localhost', port=port)
#===============================================================================
# TESTS
#===============================================================================
def test():
    print('MAPIF - TESTS NOT IMPLEMENTED')
