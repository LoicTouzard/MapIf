#!/usr/bin/python3
# -!- encoding:utf8 -!-

# --------------- IMPORTS

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy import func
from sqlalchemy import ForeignKey
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import exists
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base
import config
from src.utils import nominatim

# ----------------- CONFIG

_BASE_ = declarative_base()
_SESSIONMAKER_DEFAULT_ = None
_DBNAME_ = "general"

# ----------------- OBJECTS


class User(_BASE_):
    __tablename__ = 'user'
    __table_args__ = {'useexisting': True, 'sqlite_autoincrement': True} # <!> SQLITE <!>

    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String)
    pwd = Column(String)
    promo = Column(Integer)

    def __repr__(self):
        return "<User(id='{0}',firstname='{1}',lastname='{2}',email='{3}',promo='{4}')>".format(
            self.id, self.firstname, self.lastname, self.email, self.promo)


class Location(_BASE_):
    __tablename__ = 'location'
    __table_args__ = {'useexisting': True, 'sqlite_autoincrement': True} # <!> SQLITE <!>

    id = Column(Integer, primary_key=True, nullable=False)
    osm_id = Column(Integer)
    city = Column(String)
    country = Column(String)
    lat = Column(Float)
    lon = Column(Float)

    def __repr__(self):
        return "<Location(id='{0}',osm_id='{2}',city='{3}',country='{4}',lat='{5}',lon='{6}')>".format(
            self.id, self.osm_id, self.city, self.country, self.lat, self.lon)

class UserLocation(_BASE_):
    __tablename__ = 'user_location'
    __table_args__ = {'useexisting': True, 'sqlite_autoincrement': True} # <!> SQLITE <!>

    id = Column(Integer, primary_key=True, nullable=False)
    uid = Column(Integer, ForeignKey('user.id'))
    lid = Column(Integer, ForeignKey('location.id'))
    timestamp = Column(DateTime, default=func.now())

    def __repr__(self):
        return "<UserLocation(id='{0}',timestamp='{1}')>".format(
            self.id, self.timestamp)

# ---------------------- FUNCTIONS

def init_db():
    _database_op(_DBNAME_, create=True, drop=False)
    engine = create_engine(_get_default_database_name())
    global _SESSIONMAKER_DEFAULT_
    _SESSIONMAKER_DEFAULT_ = sessionmaker(bind=engine)
    try:
        _BASE_.metadata.create_all(engine)
    except:
        pass

"""
    Fonctions générales
"""

def _database_op(dbname, create=True, drop=False):
   if config.DATABASE == config.POSTGRE:
        db_engine = create_engine(_get_complete_database_name('postgres'))
        connection = db_engine.connect()
        connection.execute('commit')
        try:
            if create:
                connection.execute('CREATE DATABASE "{0}"'.format(dbname))
            if drop:
                connection.execute('DROP DATABASE "{0}"'.format(dbname))
        except:
            pass
        connection.close()
   elif config.DATABASE == config.SQLITE:
        if create:
            engine = create_engine(_get_complete_database_name(dbname))
            if not database_exists(engine.url):
                create_database(engine.url)
        if drop:
            remove("database/{0}.sqlite".format(dbname))

def _get_complete_database_name(database):
    if config.DATABASE == config.POSTGRE:
        return "postgresql://{0}:{1}@{2}/{3}".format(config.POSTGRE_USER, config.POSTGRE_PASS, config.POSTGRE_HOST, database)
    if config.DATABASE == config.SQLITE:
        return "sqlite:///database/{0}.sqlite".format(database)

def _get_default_database_name():
    return _get_complete_database_name(_DBNAME_)

def _get_default_db_session():
    return _SESSIONMAKER_DEFAULT_()
       
"""
  Fonctions relatives à l'utilisateur 
"""

def create_user(firstname, lastname, email, pwd, promo):
    session = _get_default_db_session()
    if not user_exists(email):
        session.add(User(firstname=firstname, lastname=lastname, email=email, pwd=pwd,promo=promo))       
        session.commit()
        session.close()
        return True
    return False

def get_all_users():
    session = _get_default_db_session()
    users = []
    for row in session.query(User).all():
        users.append(row)
    session.close()
    return users

def user_exists(email):
    session = _get_default_db_session()
    result = []
    for a in session.query(User).filter(User.email == email):
        result.append(a)
    return len(result) != 0
    
def get_user(email, pwd):
    session = _get_default_db_session()
    result = []
    for a in session.query(User).filter(User.email == email, User.pwd == pwd):
        result.append(a)
    if len(result) == 0:
        return None
    else:
        return result[0]

def add_user_location(uid, osm_id, osm_type):
    session = _get_default_db_session()
    location = get_location(osm_id)
    if not location:
        if not create_location(osm_id, osm_type):
            return False
    location = get_location(osm_id)
    session.add(UserLocation(uid=uid, lid=location.id))
    session.commit()
    session.close()
    return True

def get_location(osm_id):
    session = _get_default_db_session()
    location = session.query(Location).filter(Location.osm_id == osm_id)
    return location.first()

def create_location(osm_id, osm_type):
    session = _get_default_db_session()
    lat, lon, city, country = nominatim.reverse_location_for(osm_id, osm_type)
    if not lat or not lon or not city or not country:
        return False
    session.add(Location(osm_id=osm_id, city=city, country=country, lat=lat, lon=lon))       
    session.commit()
    session.close()
    return True

def get_user_locations(uid):
    session = _get_default_db_session()
    locations = []
    for ul in session.query(UserLocation).filter(UserLocation.uid == uid):
        l = session.query(Location).filter(Location.id == ul.lid)
        locations.append({'timestamp': ul.timestamp, 'location': l})
    return locations

def get_users_last_location():
    users = get_all_users()
    locations = []
    for u in users:
        location = get_last_location(u.id)
        locations.append({'user':u,  'location':location})
    return locations

def get_locations_with_users():
    users = get_all_users()
    locations = {}
    for u in users:
        l = get_last_location(u.id)['data']
        if l:
            str_id = '%d' % l.osm_id
            if not locations.get(str_id, None):
                locations[str_id] = {'location':l,'users':[]}
            locations[str_id]['users'].append(u)
    return list(locations.values())

def get_last_location(uid):
    session = _get_default_db_session()
    ul = session.query(UserLocation).filter(UserLocation.uid == uid).order_by(UserLocation.timestamp.desc())
    location = None
    timestamp = None
    if ul.first():
        location = session.query(Location).filter(Location.id == ul.first().lid)
        timestamp = ul.first().timestamp
    return {'timestamp': timestamp, 'data': location}

