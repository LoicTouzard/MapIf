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
        return "<User(id='{0}',firstname='{1}',lastname='{2}',email='{3}',promo='{4}')>".format(self.id, self.firstname, self.lastname, self.email, self.promo)


class Location(_BASE_):
    __tablename__ = 'location'
    __table_args__ = {'useexisting': True, 'sqlite_autoincrement': True} # <!> SQLITE <!>

    id = Column(Integer, primary_key=True, nullable=False)
    user = Column(Integer, ForeignKey('user.id'))
    timestamp = Column(DateTime, default=func.now())
    city = Column(String)
    country = Column(String)
    lat = Column(Float)
    lon = Column(Float)

    def __repr__(self):
        return "<Location(id='{0}',timestamp='{1}',city='{2}',country='{3}',lat='{4}',lon='{5}')>".format(self.id, self.timestamp, self.city, self.country, self.lat, self.lon)

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
    return (len(result) is not 0)
    
def get_user(email, pwd):
    session = _get_default_db_session()
    result = []
    for a in session.query(User).filter(User.email == email, User.pwd == pwd):
        result.append(a)
    if len(result) == 0:
        return None
    else:
        return result[0]

def create_location(user, city, country, lat, lon):
    session = _get_default_db_session()
    session.add(Location(user=user, city=city, country=country, lat=lat, lon=lon))       
    session.commit()
    session.close()

def get_user_locations(user):
    session = _get_default_db_session()
    locations = []
    for l in session.query(Location).filter(Location.user == user):
        locations.append(l)
    if len(locations) == 0 :
        return None
    else:
        return locations

def get_users_with_location():
    users = get_all_users()
    locations = []
    for u in users:
        location = get_last_location(u.id)
        temp = {'user':u,  'location':location}
        locations.append(temp)
    return locations

def get_last_location(user):
    session = _get_default_db_session()
    location = session.query(Location).filter(Location.user == user) \
        .order_by(Location.timestamp.desc())
    return location.first()