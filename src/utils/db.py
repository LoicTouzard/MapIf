#!/usr/bin/python3
# -!- encoding:utf8 -!-

# ------------------------------------------------------------------------------------------
#                                    IMPORTS & GLOBALS
# ------------------------------------------------------------------------------------------

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
from src.utils import nominatim
from src.utils import ini
from src.utils import logger

_BASE_ = declarative_base()
_SESSIONMAKER_DEFAULT_ = None

# ------------------------------------------------------------------------------------------
#                                      MODEL OBJECTS
# ------------------------------------------------------------------------------------------


class User(_BASE_):
    __tablename__ = 'user'
    __table_args__ = {'useexisting': True, 'sqlite_autoincrement': True} # <!> SQLITE <!>

    id = Column(Integer, primary_key=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, nullable=False)
    pwd = Column(String)
    promo = Column(Integer)

    def as_dict(self):
        return {
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'promo': self.promo
        }

    def __repr__(self):
        return "<User(id='{0}',firstname='{1}',lastname='{2}',email='{3}',promo='{4}')>".format(
            self.id, self.firstname, self.lastname, self.email, self.promo)


class Location(_BASE_):
    __tablename__ = 'location'
    __table_args__ = {'useexisting': True, 'sqlite_autoincrement': True} # <!> SQLITE <!>

    id = Column(Integer, primary_key=True, nullable=False)
    osm_id = Column(Integer, unique=True, nullable=False)
    city = Column(String)
    country = Column(String)
    lat = Column(Float)
    lon = Column(Float)

    def as_dict(self):
        return {
            'osm_id': self.osm_id,
            'city': self.city,
            'country': self.country,
            'lat': self.lat,
            'lon': self.lon
        }

    def __repr__(self):
        return "<Location(id='{0}',osm_id='{1}',city='{2}',country='{3}',lat='{4}',lon='{5}')>".format(
            self.id, self.osm_id, self.city, self.country, self.lat, self.lon)


class UserLocation(_BASE_):
    __tablename__ = 'user_location'
    __table_args__ = {'useexisting': True, 'sqlite_autoincrement': True} # <!> SQLITE <!>
    uid = Column(Integer, ForeignKey('user.id'), primary_key=True)
    lid = Column(Integer, ForeignKey('location.id'), primary_key=True)
    timestamp = Column(DateTime, default=func.now(), primary_key=True)

    def as_dict(self):
        return {
            'uid': self.uid,
            'lid': self.lid,
            'timestamp': self.timestamp
        }

    def __repr__(self):
        return "<UserLocation(id='{0}',timestamp='{1}')>".format(
            self.id, self.timestamp)

# ------------------------------------------------------------------------------------------
#                               INTERNAL FUNCTIONS 
# ------------------------------------------------------------------------------------------


def _database_op(dbname, action='create'):
    """
        DEPRECATED
    """
    engine = create_engine(_get_complete_database_name(dbname))
    if ini.config('DB', 'engine') == 'postgre':
        connection = engine.connect()
        connection.execute('commit')
        try:
            if action == 'create':
                if not database_exists(engine.url):
                    connection.execute('CREATE DATABASE "{0}"'.format(dbname))
            elif action == 'drop':
                connection.execute('DROP DATABASE "{0}"'.format(dbname))
        except Exception as e:
            logger.log_error('_database_op error: details below.', e)
        connection.close()
    else: # default is sqlite
        if action == 'create':
            if not database_exists(engine.url):
                create_database(engine.url)
        elif action == 'drop':
            remove("database/{0}.sqlite".format(dbname))


def _get_complete_database_name(database):
    url = None
    if ini.config('DB', 'engine') == 'postgre':
        if ini.getenv('OPENSHIFT_POSTGRESQL_DB_URL'):
            url = ini.getenv('OPENSHIFT_POSTGRESQL_DB_URL')
        else:
            url = "postgresql://{0}:{1}@{2}/{3}".format(
                ini.config('DB', 'postgre_user'),
                ini.config('DB', 'postgre_pass'),
                ini.config('DB', 'postgre_host'), database)
    elif ini.config('DB', 'engine') == 'sqlite':
        url = "sqlite:///database/{0}.sqlite".format(database)
    return url


def _get_default_database_name():
    return _get_complete_database_name(ini.config('DB', 'db_name'))


def _get_default_db_session():
    return _SESSIONMAKER_DEFAULT_()

# ------------------------------------------------------------------------------------------
#                               EXTERN FUNCTIONS
# ------------------------------------------------------------------------------------------


def init_db():
    """
        Initializes MapIf database.
    """
    #_database_op(ini.config('DB', 'db_name'), action='create') # DEPRECATED : ensure database exists before launching application
    engine = create_engine(_get_default_database_name())
    global _SESSIONMAKER_DEFAULT_
    _SESSIONMAKER_DEFAULT_ = sessionmaker(bind=engine)
    try:
        _BASE_.metadata.create_all(engine)
        logger.mprint("DB module successfully initialized.")
    except Exception as e:
        logger.log_error('init_db error: details below.', e)


def create_user(firstname, lastname, email, pwd, promo):
    """
        Creates a user and insert it in the database
    """
    ok = False
    session = _get_default_db_session()
    if not user_exists(email):
        session.add(User(firstname=firstname, lastname=lastname, email=email, pwd=pwd,promo=promo))       
        session.commit()
        ok = True
    session.close()
    return ok


def get_all_users():
    """
        Returns a list of all users registered in the database
    """
    session = _get_default_db_session()
    users = []
    for row in session.query(User).all():
        users.append(row)
    session.close()
    return users


def user_exists(email):
    """
        Checks if a user already exists using given email
    """
    session = _get_default_db_session()
    result = []
    for row in session.query(User).filter(User.email == email):
        result.append(row)
    session.close()
    return len(result) != 0

    
def get_user(email, pwd):
    """
        Returns the user matching both email and password (hashed) or None
    """
    session = _get_default_db_session()
    result = []
    for row in session.query(User).filter(User.email == email, User.pwd == pwd):
        result.append(row)
    session.close()
    return None if len(result) == 0 else result[0]


def add_user_location(uid, osm_id, osm_type):
    """
        Adds location for the user having matching uid
    """
    session = _get_default_db_session()
    location = get_location(osm_id)
    if not location:
        if not create_location(osm_id, osm_type):
            return False # interrupt here
    location = get_location(osm_id)
    session.add(UserLocation(uid=uid, lid=location.id))
    session.commit()
    session.close()
    return True


def get_location(osm_id):
    """
        Searches the database location matching the given osm_id
    """
    session = _get_default_db_session()
    location = session.query(Location).filter(Location.osm_id == osm_id)
    session.close()
    return location.first()


def create_location(osm_id, osm_type):
    """
        Creates a new location using given osm_id and osm_type to get 
        valid information from nominatim API
    """
    ok = True
    session = _get_default_db_session()
    lat, lon, city, country = nominatim.reverse_location_for(osm_id, osm_type)
    if not lat or not lon or not city or not country:
        logger.log_error('Incomplete location returned by Nominatim (lat={0},lon={1},city={2},country={3})'.format(lat,lon,city,country))
        ok = False
    else:
        session.add(Location(osm_id=osm_id, city=city, country=country, lat=lat, lon=lon))       
        session.commit()
    session.close()
    return ok


def get_user_locations(uid):
    """
        Returns a list of locations for the given user with the associated 
        timestamp
    """
    session = _get_default_db_session()
    locations = []
    for ul in session.query(UserLocation).filter(UserLocation.uid == uid):
        l = session.query(Location).filter(Location.id == ul.lid)
        locations.append({'timestamp': ul.timestamp, 'location': l.first().as_dict()})
    session.close()
    return locations


def get_users_lastest_location():
    """
        Gets a list of users latest location
    """
    locations = []
    for u in get_all_users():
        location = get_lastest_location(u.id)
        locations.append({'user':u,  'location':location})
    return locations


def get_locations_with_users():
    """
        Returns a list of user having the same latest location indexed with this location
    """
    locations = {}
    for u in get_all_users():
        l = get_lastest_location(u.id)['data']
        if l:
            str_id = '%d' % l.osm_id
            if not locations.get(str_id, None):
                locations[str_id] = {'location':l,'users':[]}
            locations[str_id]['users'].append(u)
    return list(locations.values())


def get_lastest_location(uid):
    """
        Returns the latest location added by the user matching given id
    """
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


def delete_user(uid):
    """
        Erases all data related to user's given id, data is definitly lost
    """
    session = _get_default_db_session()
    session.query(UserLocation).filter(UserLocation.uid == uid).delete()
    session.query(User).filter(User.id == uid).delete()
    session.commit()
    session.close()

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

def test():
    """
        Module unit tests
    """
    print('DB - TESTS NOT IMPLEMENTED')
