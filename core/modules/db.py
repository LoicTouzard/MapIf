#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: db.py
#    date: 2017-09-22
# authors: paul.dautry, ...
# purpose:
#   
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
import re
import json
import bcrypt
import hashlib
from datetime                               import datetime
from sqlalchemy                             import create_engine
from sqlalchemy_utils                       import database_exists
from sqlalchemy_utils                       import create_database
from sqlalchemy.sql                         import exists
from core.modules                           import ini
from core.modules                           import logger
from core.modules                           import nominatim
from core.modules.validator                 import normalize_filter
from core.classes.model.session             import MapifSession
from core.classes.model.base                import MapifBase
from core.classes.model.user                import User
from core.classes.model.user                import UserCRUD
from core.classes.model.location            import Location
from core.classes.model.location            import LocationCRUD
from core.classes.model.user_location       import UserLocation
from core.classes.model.user_location       import UserLocationCRUD
from core.classes.model.password_reset      import PasswordReset
from core.classes.model.password_reset      import PasswordResetCRUD
from core.classes.model.user_preferences    import UserPreferences
from core.classes.model.user_preferences    import UserPreferencesCRUD
#===============================================================================
# GLOBALS
#===============================================================================
modlgr = logger.get('mapif.db')
META_REASON_ENUM = [
    'no', 
    'internship', 
    'exchange', 
    'dd', 
    'job', 
    'vacation'
]
#===============================================================================
# MODEL OBJECTS
#===============================================================================
#-------------------------------------------------------------------------------
# _get_complete_database_name
#-------------------------------------------------------------------------------
def _get_complete_database_name(database):
    url = None
    if ini.config('DB', 'engine') == 'postgre':
        if ini.getenv('MAPIF_POSTGRESQL_DB_URL'):
            url = ini.getenv('MAPIF_POSTGRESQL_DB_URL')
        else:
            url = "postgresql://{0}:{1}@{2}/{3}".format(
                ini.config('DB', 'postgre_user'),
                ini.config('DB', 'postgre_pass'),
                ini.config('DB', 'postgre_host'), 
                database)
    elif ini.config('DB', 'engine') == 'sqlite':
        url = "sqlite:///database/{0}.sqlite".format(database)
    return url
#-------------------------------------------------------------------------------
# _get_default_database_name
#-------------------------------------------------------------------------------
def _get_default_database_name():
    return _get_complete_database_name(ini.config('DB', 'db_name'))
#-------------------------------------------------------------------------------
# init_db
#   Initializes MapIf database.
#-------------------------------------------------------------------------------
def init():
    try:
        engine = create_engine(_get_default_database_name())
        MapifSession.configure(bind=engine)
        MapifBase.metadata.create_all(engine)
    except Exception as e:
        modlgr.exception('db.init() error!')
        return False
    modlgr.debug("DB module successfully initialized.")
    return True
#===============================================================================
# User CRUD ops
#===============================================================================
#-------------------------------------------------------------------------------
# create_user
#   Creates a user and insert it in the database
#-------------------------------------------------------------------------------
def create_user(firstname, lastname, email, pwd, promo):
    status = False
    email = email.lower()
    if not user_exists(email):
        hashedpwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
        UserCRUD.create(firstname, lastname, email, hashedpwd, promo)
        return True
    return False
#-------------------------------------------------------------------------------
# retrieve_user_by_id
#   Returns the user having the given uid or None
#-------------------------------------------------------------------------------
def retrieve_user_by_id(uid):
    (s, q) = UserCRUD.retrieve(uid=uid)
    res = q.one_or_none()
    s.close()
    return res
#-------------------------------------------------------------------------------
# retrieve_user_by_email
#   Returns the user having the given email or None
#-------------------------------------------------------------------------------
def retrieve_user_by_email(email):
    email = email.lower()
    (s, q) = UserCRUD.retrieve(email=email)
    res = q.one_or_none()
    s.close()
    return res
#-------------------------------------------------------------------------------
# retrieve_all_users
#   Returns a list of all users registered in the database
#-------------------------------------------------------------------------------
def retrieve_all_users():
    (s, q) = UserCRUD.retrieve()
    res = q.all()
    s.close()
    return res
#-------------------------------------------------------------------------------
# search_users
#   Retrieve user based on search filters
#-------------------------------------------------------------------------------
def search_users(filters):
    # retrieve and normalize filters
    promo_filter = normalize_filter(filters.get('promo', None))
    firstname_filter = normalize_filter(filters.get('firstname', None))
    lastname_filter = normalize_filter(filters.get('lastname', None))
    return UserCRUD.search(firstname_filter, lastname_filter, promo_filter)
#-------------------------------------------------------------------------------
# update_user
#   Updates a user in the database
#-------------------------------------------------------------------------------
def update_user(uid, **kwargs):
    return UserCRUD.update(uid, **kwargs)
#-------------------------------------------------------------------------------
# delete_user
#   Erases all data related to user's given id, data is definitly lost
#-------------------------------------------------------------------------------
def delete_user(uid):
    UserLocationCRUD.delete(uid=uid)
    UserPreferencesCRUD.delete(uid=uid)
    UserCRUD.delete(uid=uid)
#===============================================================================
# Location CRUD ops
#===============================================================================
#-------------------------------------------------------------------------------
# create_location
#-------------------------------------------------------------------------------
def create_location(osm_id, osm_type):
    status = True
    lat, lon, city, country = nominatim.reverse_location_for(osm_id, osm_type)
    if not lat or not lon or not city or not country:
        modlgr.error("""incomplete location returned by Nominatim (lat={0},lon={1},city={2},country={3})""".format(lat,lon,city,country))
        status = False
    else:
        LocationCRUD.create(osm_id, city, country, lat, lon)
    return status
#-------------------------------------------------------------------------------
# retrieve_location
#-------------------------------------------------------------------------------
def retrieve_location(osm_id):
    (s, q) = LocationCRUD.retrieve(osm_id=osm_id)
    # /!\ inconsistent DB: clear DB and use one_or_none() instead
    loc = q.first() 
    s.close()
    return loc
#-------------------------------------------------------------------------------
# update_location
#-------------------------------------------------------------------------------
def update_location(lid, **kwargs):
    return LocationCRUD.update(lid, **kwargs)
#-------------------------------------------------------------------------------
# delete_location
#-------------------------------------------------------------------------------
def delete_location(lid):
    LocationCRUD.delete(lid)
#===============================================================================
# UserPreferences CRUD ops
#===============================================================================
#-------------------------------------------------------------------------------
# create_user_preferences
#-------------------------------------------------------------------------------
def create_user_preferences(uid):
    UserPreferencesCRUD.create(uid, False, False)
#-------------------------------------------------------------------------------
# retrieve_user_preferences
#-------------------------------------------------------------------------------
def retrieve_user_preferences(uid):
    (s, q) = UserPreferencesCRUD.retrieve(uid=uid)
    res = q.one_or_none()
    s.close()
    return res
#-------------------------------------------------------------------------------
# update_user_preferences
#-------------------------------------------------------------------------------
def update_user_preferences(uid, **kwargs):
    return UserPreferencesCRUD.update(uid, **kwargs)
#-------------------------------------------------------------------------------
# delete_user_preferences
#-------------------------------------------------------------------------------
def delete_user_preferences(uid):
    UserPreferencesCRUD.delete(uid)
#===============================================================================
# UserLocation CRUD ops
#===============================================================================
#-------------------------------------------------------------------------------
# create_user_location
#   Adds location for the user matching uid
#-------------------------------------------------------------------------------
def create_user_location(uid, osm_id, osm_type, metadata):
    loc = retrieve_location(osm_id)
    if not loc:
        if not create_location(osm_id, osm_type):
            return False # interrupt here, Nominatim failed...
    loc = retrieve_location(osm_id)
    UserLocationCRUD.create(uid, loc.id, datetime.now(), meta=json.dumps([metadata]))
    return True
#-------------------------------------------------------------------------------
# retrieve_lastest_location
#   Returns the latest location added by the user matching given id
#-------------------------------------------------------------------------------
def retrieve_user_lastest_location(uid):
    (s, q) = UserLocationCRUD.retrieve(uid=uid)
    ul = q.order_by(UserLocation.timestamp.desc()).first()
    s.close()
    loc = None
    timestamp = None
    if ul is not None:
        timestamp = ul.timestamp
        (s, q) = LocationCRUD.retrieve(lid=ul.lid)
        loc = q.first()
        s.close()
    return {
        'timestamp': timestamp, 
        'data': loc
    }
#-------------------------------------------------------------------------------
# retrieve_user_locations
#   Returns a list of locations for the given user with the associated 
#   timestamp
#-------------------------------------------------------------------------------
def retrieve_user_locations(uid):
    locs = []
    (s1, q1) = UserLocationCRUD.retrieve(uid=uid)
    for ul in q1:
        (s2, q2) = LocationCRUD.retrieve(lid=ul.lid)
        loc = q2.first()
        s2.close()
        locs.append({
            'ulid': ul.id, 
            'timestamp': ul.timestamp, 
            'location': loc.as_dict()
        })
    s1.close()
    return locs
#-------------------------------------------------------------------------------
# update_user_location
#   Updates user location timestamp
#-------------------------------------------------------------------------------
def update_user_location(uid, ulid, timestamp, metadata):
    return UserLocationCRUD.update(uid, ulid, 
        timestamp=datetime.now(), meta=json.dumps(metadata))
#-------------------------------------------------------------------------------
# delete_user_location
#   Deletes the given user location
#-------------------------------------------------------------------------------
def delete_user_location(uid, ulid):
    # SEC-NOTE: test ulid and uid, even if uid is a foreign key, to prevent a 
    #           user deleting a record of another user.
    UserLocationCRUD.delete(uid=uid, ulid=ulid)
#===============================================================================
# PasswordReset CRUD ops
#===============================================================================
#-------------------------------------------------------------------------------
# create_or_update_password_reset
#-------------------------------------------------------------------------------
def create_or_update_password_reset(email, hashing_key):
    timestamp = datetime.now()
    token_str = "{0}{1}{2}".format(email, timestamp, hashing_key)
    token = hashlib.sha1(token_str.encode()).hexdigest()
    usr = retrieve_user_by_email(email)
    (s, q) = PasswordReset.retrieve(uid=usr.id)
    pwrst = q.one_or_none()
    s.close()
    if pwrst is None:
        PasswordResetCRUD.create(usr.id, token, timestamp, False)
    else:
        PasswordResetCRUD.update(usr.id, 
            token=token, timestamp=timestamp, used=False)
    return token
#-------------------------------------------------------------------------------
# retrieve_password_reset
#-------------------------------------------------------------------------------
def retrieve_password_reset(uid, token):
    (s, q) = PasswordResetCRUD.retrieve(uid=uid, token=token)
    res = q.one_or_none()
    s.close()
    return res
#-------------------------------------------------------------------------------
# set_password_reset_used
#-------------------------------------------------------------------------------
def set_password_reset_used(uid):
    return PasswordResetCRUD.update(uid, used=True)
#===============================================================================
# Shorthand functions
#===============================================================================
#-------------------------------------------------------------------------------
# user_exists
#   Checks if a user already exists using given email
#-------------------------------------------------------------------------------
def user_exists(email):
    return (retrieve_user_by_email(email) is not None)
#-------------------------------------------------------------------------------
# retrieve_user_email_pwd
#   Returns the user matching both email and password (hashed) or None
#-------------------------------------------------------------------------------
def retrieve_user_email_pwd(email, sha_pwd):
    usr = retrieve_user_by_email(email)
    if usr is not None:
        # fix issue #14: safe password storage with salt and blowfish encryption
        if usr.pwd != bcrypt.hashpw(sha_pwd.encode(), usr.pwd.encode()).decode():
            usr = None
    return usr
#-------------------------------------------------------------------------------
# check_user_password
#   Checks if user password is correct
#-------------------------------------------------------------------------------
def check_user_password(uid, sha_pwd):
    usr = retrieve_user_by_id(uid)
    if usr is not None:
        return (usr.pwd != bcrypt.hashpw(sha_pwd.encode(), usr.pwd.encode()).decode())
    return False
#-------------------------------------------------------------------------------
# retrieve_users_lastest_location
#   Gets a list of users latest location
#-------------------------------------------------------------------------------
def retrieve_users_lastest_location():
    locs = []
    for u in retrieve_all_users():
        loc = retrieve_user_lastest_location(u.id)
        locs.append({
            'user': u,  
            'location': loc
        })
    return locs
#-------------------------------------------------------------------------------
# retrieve_locations_with_users
#   Returns a list of user having the same latest location indexed on this 
#   location
#-------------------------------------------------------------------------------
def retrieve_locations_with_users():
    locations = {}
    for u in retrieve_all_users():
        l = retrieve_user_lastest_location(u.id)['data']
        if l:
            str_id = '%s' % l.osm_id
            if not locations.get(str_id, None):
                locations[str_id] = {
                    'location': l,
                    'users': []
                }
            locations[str_id]['users'].append(u)
    return list(locations.values())
#===============================================================================
# MAINTENANCE FUNCTIONS
#===============================================================================
# none
#===============================================================================
# TESTS
#===============================================================================
def test():
    print('DB - TESTS NOT IMPLEMENTED')
