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
from sqlalchemy              import Column
from sqlalchemy              import Integer
from sqlalchemy              import String
from sqlalchemy              import Float
from core.classes.model.base import MapifBase
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