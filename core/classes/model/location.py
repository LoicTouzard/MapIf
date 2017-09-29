#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: user.py
#    date: 2017-09-26
#  author: paul.dautry
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
from sqlalchemy                 import Column
from sqlalchemy                 import Integer
from sqlalchemy                 import String
from sqlalchemy                 import Float
from core.classes.model.base    import MapifBase
from core.classes.model.session import session
from core.modules               import logger
#===============================================================================
# GLOBALS
#===============================================================================
modlgr = logger.get('mapif.location')
#===============================================================================
# CLASSES
#===============================================================================
#-------------------------------------------------------------------------------
# Location
#-------------------------------------------------------------------------------
class Location(MapifBase):
    __tablename__ = 'location'
    __table_args__ = {
            'useexisting': True, 
            'sqlite_autoincrement': True # <!> SQLITE <!>
    }
    #---------------------------------------------------------------------------
    # attributes
    #---------------------------------------------------------------------------
    id = Column(Integer, primary_key=True, nullable=False)
    osm_id = Column(String, unique=True, nullable=False)
    city = Column(String)
    country = Column(String)
    lat = Column(Float)
    lon = Column(Float)
    #---------------------------------------------------------------------------
    # as_dict
    #---------------------------------------------------------------------------
    def as_dict(self):
        return {
            'osm_id': self.osm_id,
            'city': self.city,
            'country': self.country,
            'lat': self.lat,
            'lon': self.lon
        }
    #---------------------------------------------------------------------------
    # __repr__
    #---------------------------------------------------------------------------
    def __repr__(self):
        return """<Location(id='{0}',
    osm_id='{1}',
    city='{2}',
    country='{3}',
    lat='{4}', lon='{5}'
)>""".format(self.id, self.osm_id, self.city, self.country, self.lat, self.lon)
#-------------------------------------------------------------------------------
# LocationCRUD
#-------------------------------------------------------------------------------
class LocationCRUD:
    ATTRIBUTES = [
        'osm_id',
        'city',
        'country',
        'lat',
        'lon'
    ]
    #---------------------------------------------------------------------------
    # __apply_filters
    #---------------------------------------------------------------------------
    @staticmethod
    def __apply_filters(q, **kwargs):
        for key, val in kwargs.items():
            if val is not None:
                if key == 'lid': 
                    q = q.filter(Location.id == val)
                elif key == 'osm_id':
                    q = q.filter(Location.osm_id == val)
                elif key == 'city':
                    q = q.filter(Location.city == val)
                elif key == 'country':
                    q = q.filter(Location.country == val)
                elif key == 'lat':
                    q = q.filter(Location.lat == val)
                elif key == 'lon':
                    q = q.filter(Location.lon == val)
                else:
                    modlgr.warning('retrieve() argument "{0}" will be ignored.'.format(
                        key))
        return q
    #---------------------------------------------------------------------------
    # create 
    #---------------------------------------------------------------------------
    @staticmethod
    def create(osm_id, city, country, lat, lon):
        s = session()
        s.add(Location(osm_id=osm_id, city=city, country=country, lat=lat, lon=lon))
        s.commit()
        s.close()
    #---------------------------------------------------------------------------
    # retrieve 
    #---------------------------------------------------------------------------
    @staticmethod
    def retrieve(**kwargs):
        s = session()
        q = s.query(Location)
        q = LocationCRUD.__apply_filters(q, **kwargs)
        return (s, q)
    #---------------------------------------------------------------------------
    # update
    #---------------------------------------------------------------------------
    @staticmethod
    def update(lid, **kwargs):
        state = False
        s = session()
        loc = s.query(Location).filter(Location.id == lid).one_or_none()
        if loc is not None:
            for key, val in kwargs.items():
                if val is not None and key in LocationCRUD.ATTRIBUTES:
                    if key == 'id':
                        modlgr.warning('update() cannot update id.')
                        continue
                    setattr(loc, key, val)
            s.add(loc)
            s.commit()
            state = True
        s.close()
        return state
    #---------------------------------------------------------------------------
    # delete 
    #---------------------------------------------------------------------------
    @staticmethod
    def delete(**kwargs):
        s = session()
        q = s.query(Location)
        q = LocationCRUD.__apply_filters(q, **kwargs)
        q.delete()
        s.commit()
        s.close()
