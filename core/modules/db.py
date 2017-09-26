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
from datetime                           import datetime
from sqlalchemy                         import create_engine
from sqlalchemy_utils                   import database_exists
from sqlalchemy_utils                   import create_database
from sqlalchemy.orm                     import sessionmaker
from sqlalchemy.sql                     import exists
from sqlalchemy.schema                  import MetaData
from sqlalchemy.ext.declarative         import declarative_base
from core.classes.model.user            import User
from core.classes.model.location        import Location
from core.classes.model.user_location   import UserLocation
from core.classes.model.password_reset  import PasswordReset
from core.modules                       import ini
from core.modules                       import logger
from core.modules                       import nominatim
#===============================================================================
# GLOBALS
#===============================================================================
modlgr = logger.get('mapif.db')
_SESSIONMAKER_DEFAULT_ = None
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
# _get_default_db_session
#-------------------------------------------------------------------------------
def _get_default_db_session():
    return _SESSIONMAKER_DEFAULT_()
#-------------------------------------------------------------------------------
# init_db
#   Initializes MapIf database.
#-------------------------------------------------------------------------------
def init():
    #_database_op(ini.config('DB', 'db_name'), action='create') # DEPRECATED : ensure database exists before launching application
    engine = create_engine(_get_default_database_name())
    global _SESSIONMAKER_DEFAULT_
    _SESSIONMAKER_DEFAULT_ = sessionmaker(bind=engine)
    try:
        declarative_base().metadata.create_all(engine)
        modlgr.debug("DB module successfully initialized.")
    except Exception as e:
        modlgr.exception('init_db error!')
#-------------------------------------------------------------------------------
# create_user
#   Creates a user and insert it in the database
#-------------------------------------------------------------------------------
def create_user(firstname, lastname, email, pwd, promo):
    status = False
    session = _get_default_db_session()
    if not user_exists(email):
        hashedpwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode()
        session.add(User(firstname=firstname, lastname=lastname, email=email.lower(), pwd=hashedpwd, promo=promo))
        session.commit()
        status = True
    session.close()
    return status
#-------------------------------------------------------------------------------
# update_user
#   Updates a user in the database
#-------------------------------------------------------------------------------
def update_user(uid, **kwargs):
    status = False
    session = _get_default_db_session()
    user = session.query(User).filter(User.id == uid).one()
    if user != []:
        for key,value in kwargs.items():
            if key in ['firstname','lastname','email','pwd','promo'] and value is not None:
                if key == 'pwd':
                    value = bcrypt.hashpw(value.encode(), bcrypt.gensalt()).decode()
                setattr(user, key, value)
        session.add(user)
        session.commit()
        status = True
    return status
#-------------------------------------------------------------------------------
# get_all_users
#   Returns a list of all users registered in the database
#-------------------------------------------------------------------------------
def get_all_users():
    session = _get_default_db_session()
    users = []
    for row in session.query(User).all():
        users.append(row)
    session.close()
    return users
#-------------------------------------------------------------------------------
# user_exists
#   Checks if a user already exists using given email
#-------------------------------------------------------------------------------
def user_exists(email):
    session = _get_default_db_session()
    result = []
    for row in session.query(User).filter(User.email == email.lower()):
        result.append(row)
    session.close()
    return len(result) != 0
#-------------------------------------------------------------------------------
# get_user
#   Returns the user matching both email and password (hashed) or None
#-------------------------------------------------------------------------------
def get_user(email, sha_pwd):
    session = _get_default_db_session()
    # retrieve user using email
    user = session.query(User).filter(User.email == email.lower()).one_or_none()
    session.close()
    if user is not None:
        # fix issue #14: safe password storage with salt and blowfish encryption
        if user.pwd != bcrypt.hashpw(sha_pwd.encode(), user.pwd.encode()).decode():
            user = None
    return user
#-------------------------------------------------------------------------------
# get_user_by_id
#   Returns the user having the given uid or None
#-------------------------------------------------------------------------------
def get_user_by_id(uid):
    session = _get_default_db_session()
    user = session.query(User).filter(User.id == uid).one_or_none()
    session.close()
    return user
#-------------------------------------------------------------------------------
# get_user_by_email
#   Returns the user having the given email or None
#-------------------------------------------------------------------------------
def get_user_by_email(email):
    session = _get_default_db_session()
    user = session.query(User).filter(User.email == email.lower()).one_or_none()
    session.close()
    return user
#-------------------------------------------------------------------------------
# check_user_password
#   Checks if user password is correct
#-------------------------------------------------------------------------------
def check_user_password(uid, sha_pwd):
    user = get_user_by_id(uid)
    if user is not None:
        return (user.pwd != bcrypt.hashpw(sha_pwd.encode(), user.pwd.encode()).decode())
    return False
#-------------------------------------------------------------------------------
# get_password_reset_by_token_and_uid
#   
#-------------------------------------------------------------------------------
def get_password_reset_by_token_and_uid(token, user_id):
    session = _get_default_db_session()
    pwd_reset = session.query(PasswordReset).filter(PasswordReset.token == token).filter(PasswordReset.uid == user_id).one_or_none()
    session.close()
    return pwd_reset
#-------------------------------------------------------------------------------
# set_password_reset_used
#
#-------------------------------------------------------------------------------
def set_password_reset_used(password_reset):
    session = _get_default_db_session()
    setattr(password_reset, 'used', True)
    session.add(password_reset)
    session.commit()
    session.close()
#-------------------------------------------------------------------------------
# normalize_filter
#   Treat filter content to create a valid SQL filter string
#-------------------------------------------------------------------------------
def normalize_filter(search_filter):
    if search_filter is not None:
        # remove forbidden characters
        search_filter = re.sub('[^*a-zA-Z0-9]', '', search_filter)
        # replace special characters
        search_filter = search_filter.replace('*', '%')
    else:
        search_filter = '%'
    return search_filter
#-------------------------------------------------------------------------------
# get_users
#   Retrieve user based on search filters
#-------------------------------------------------------------------------------
def get_users(filters):
    # retrieve and normalize filters
    promo_filter = normalize_filter(filters.get('promo', None))
    firstname_filter = normalize_filter(filters.get('firstname', None))
    lastname_filter = normalize_filter(filters.get('lastname', None))
    # retrieve session
    session = _get_default_db_session()
    return session.query(User).filter(
        User.promo.ilike(promo_filter),
        User.firstname.ilike(firstname_filter),
        User.lastname.ilike(lastname_filter)).all()
#-------------------------------------------------------------------------------
# create_user_location
#   Adds location for the user matching uid
#-------------------------------------------------------------------------------
def create_user_location(uid, osm_id, osm_type, metadata):
    session = _get_default_db_session()
    location = get_location(osm_id)
    if not location:
        if not create_location(osm_id, osm_type):
            return False # interrupt here
    location = get_location(osm_id)
    session.add(UserLocation(uid=uid, lid=location.id, meta=json.dumps([metadata])))
    session.commit()
    session.close()
    return True
#-------------------------------------------------------------------------------
# update_user_location
#   Updates user location timestamp
#-------------------------------------------------------------------------------
def update_user_location(uid, ulid, timestamp, metadata):
    status = False
    session = _get_default_db_session()
    dateobj = datetime.strpfmt(timestamp, '%Y-%m-%d')
    # SEC-NOTE: test ulid and uid, even if uid is a foreign key, to prevent a 
    #           user updating a record of another user.
    q = session.query(UserLocation).filter(
        UserLocation.id == ulid, 
        UserLocation.uid == uid).one()
    if q != []:
        q.timestamp = dateobj
        q.meta = json.dumps([metadata])
        session.add(q)
        session.commit()
        status = True
    return status
#-------------------------------------------------------------------------------
# delete_user_location
#   Deletes the given user location
#-------------------------------------------------------------------------------
def delete_user_location(uid, ulid):
    status = False
    session = _get_default_db_session()
    # SEC-NOTE: test ulid and uid, even if uid is a foreign key, to prevent a 
    #           user deleting a record of another user.
    session.query(UserLocation).filter(
        UserLocation.id == ulid, 
        UserLocation.uid == uid).delete()
    session.commit()
    session.close()
#-------------------------------------------------------------------------------
# get_location
#   Searches the database location matching the given osm_id
#-------------------------------------------------------------------------------
def get_location(osm_id):
    session = _get_default_db_session()
    location = session.query(Location).filter(Location.osm_id == osm_id)
    session.close()
    return location.first()
#-------------------------------------------------------------------------------
# create_location
#   Creates a new location using given osm_id and osm_type to get 
#   valid information from nominatim API
#-------------------------------------------------------------------------------
def create_location(osm_id, osm_type):
    status = True
    session = _get_default_db_session()
    lat, lon, city, country = nominatim.reverse_location_for(osm_id, osm_type)
    if not lat or not lon or not city or not country:
        modlgr.error('Incomplete location returned by Nominatim (lat={0},lon={1},city={2},country={3})'.format(lat,lon,city,country))
        status = False
    else:
        session.add(Location(osm_id=osm_id, city=city, country=country, lat=lat, lon=lon))       
        session.commit()
    session.close()
    return status
#-------------------------------------------------------------------------------
# get_user_locations
#   Returns a list of locations for the given user with the associated 
#   timestamp
#-------------------------------------------------------------------------------
def get_user_locations(uid):
    session = _get_default_db_session()
    locations = []
    for ul in session.query(UserLocation).filter(UserLocation.uid == uid):
        l = session.query(Location).filter(Location.id == ul.lid).first()
        locations.append({'timestamp': ul.timestamp, 'location': l.as_dict()})
    session.close()
    return locations
#-------------------------------------------------------------------------------
# get_users_lastest_location
#   Gets a list of users latest location
#-------------------------------------------------------------------------------
def get_users_lastest_location():
    locations = []
    for u in get_all_users():
        location = get_lastest_location(u.id)
        locations.append({'user':u,  'location':location})
    return locations
#-------------------------------------------------------------------------------
# get_locations_with_users
#   Returns a list of user having the same latest location indexed with this location
#-------------------------------------------------------------------------------
def get_locations_with_users():
    locations = {}
    for u in get_all_users():
        l = get_lastest_location(u.id)['data']
        if l:
            str_id = '%s' % l.osm_id
            if not locations.get(str_id, None):
                locations[str_id] = {'location':l,'users':[]}
            locations[str_id]['users'].append(u)
    return list(locations.values())
#-------------------------------------------------------------------------------
# get_lastest_location
#   Returns the latest location added by the user matching given id
#-------------------------------------------------------------------------------
def get_lastest_location(uid):
    session = _get_default_db_session()
    ul = session.query(UserLocation).filter(UserLocation.uid == uid).order_by(UserLocation.timestamp.desc())
    location = None
    timestamp = None
    if ul.first():
        location = session.query(Location).filter(Location.id == ul.first().lid)
        if location:
            location = location.first()
        timestamp = ul.first().timestamp
    session.close()
    return {'timestamp': timestamp, 'data': location}
#-------------------------------------------------------------------------------
# delete_user
#   Erases all data related to user's given id, data is definitly lost
#-------------------------------------------------------------------------------
def delete_user(uid):
    session = _get_default_db_session()
    session.query(UserLocation).filter(UserLocation.uid == uid).delete()
    session.query(User).filter(User.id == uid).delete()
    session.commit()
    session.close()
    return True
#-------------------------------------------------------------------------------
# create_or_update_password_reset
#-------------------------------------------------------------------------------
def create_or_update_password_reset(email, additional_hashing_key):
    session = _get_default_db_session()
    current_timestamp = datetime.now()
    hashed_value = hashlib.sha1(("{0}{1}{2}".format(email, current_timestamp, additional_hashing_key)).encode()).hexdigest()
    user = get_user_by_email(email)
    passwd_reset = session.query(PasswordReset).filter(PasswordReset.uid == user.id).one_or_none()
    if passwd_reset is None:  # Create object
        session.add(PasswordReset(uid=user.id, token=hashed_value, timestamp=current_timestamp, used=False))
    else:  # Update object
        setattr(passwd_reset, 'token', hashed_value)
        setattr(passwd_reset, 'timestamp', current_timestamp)
        setattr(passwd_reset, 'used', False)
        session.add(passwd_reset)
    session.commit()
    session.close()
    return hashed_value
#===============================================================================
# MAINTENANCE FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# update_user_password
#   fix issue #14: safe password storage with salt and blowfish encryption
#-------------------------------------------------------------------------------
#def update_user_password(uid):
#    session = _get_default_db_session()
#    user = session.query(User).filter(User.id == uid).one_or_none()
#    user.pwd = bcrypt.hashpw(user.pwd.encode(), bcrypt.gensalt()).decode()
#    session.add(user)
#    session.commit()
#    session.close()
#===============================================================================
# TESTS
#===============================================================================
def test():
    print('DB - TESTS NOT IMPLEMENTED')
