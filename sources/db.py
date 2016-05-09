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
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import config

# ----------------- CONFIG

_BASE_ = declarative_base()
_SESSIONMAKER_DEFAULT_ = None
_DBNAME_ = 'general'

# ----------------- OBJECTS

class User(Base):
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

class Location(Base):
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
           create_engine(_get_complete_database_name(dbname))
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

def init_db():
    _database_op(_DBNAME_, create=True)
    engine = create_engine(_get_default_database_name())
    global _SESSIONMAKER_DEFAULT_
    _SESSIONMAKER_DEFAULT_ = sessionmaker(bind=engine)
    try:
        _BASE_.metadata.create_all(engine)
    except:
        pass


