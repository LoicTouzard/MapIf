#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: nominatim.py
#    date: 2017-09-22
# authors: paul.dautry, ...
# purpose:
#       Defines some functions to interact with Nominatim API
#       (an OpenStreetMap service)
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
import requests
import json
from urllib.parse import quote
from core.utils import logger
#===============================================================================
# GLOBALS
#===============================================================================
_SEARCH_BASE_URL_ = "http://nominatim.openstreetmap.org/search/"
_SEARCH_PARAMS_ = {
    'format': 'json',
    'addressdetails':'1',
    'limit':'1'
}
_REVERSE_BASE_URL_ = "http://nominatim.openstreetmap.org/reverse"
_REVERSE_PARAMS_ = {
    'format': 'json',
    'addressdetails':'1'
}
_OSM_TYPES_ = {
    'way': 'W',
    'node': 'N',
    'relation': 'R'
}
#===============================================================================
# FUNCTIONS
#===============================================================================
#-------------------------------------------------------------------------------
# location_for
#   Search a latitude and longitude for the given city and country using 
#   Nominatim API
#-------------------------------------------------------------------------------
def location_for(city, country):
    url = _SEARCH_BASE_URL_ + quote('{city} {country}'.format(city=city, country=country))
    resp = requests.get(url, params=_SEARCH_PARAMS_)
    data = json.loads(resp.text)
    lat = None
    lon = None
    city = None
    country = None
    if len(data) > 0:
        lat = data[0].get('lat', None)
        lon = data[0].get('lon', None)
        address = data[0].get('address', None)
        if address: 
            city = address.get('city', None)
            country = address.get('country', None)
    return (lat, lon, city, country) 
#-------------------------------------------------------------------------------
# reverse_location_for
#   Retrieve information related with the given osm_id and osm_type using 
#   Nominatim API
#-------------------------------------------------------------------------------
def reverse_location_for(osm_id, osm_type):
    params = _REVERSE_PARAMS_
    params['osm_id'] = osm_id
    params['osm_type'] = _OSM_TYPES_.get(osm_type, None)
    resp = requests.get(_REVERSE_BASE_URL_, params=params)
    data = json.loads(resp.text)
    lat = None
    lon = None
    city = None
    country = None
    if not data.get('error', None):
        lat = data['lat']
        lon = data['lon']
        address = data.get('address', None)
        if address: 
            city = address.get('city', None)
            if not city:
                # problem for Dublin Issue #4 (osm_id=3473474851, osm_type=N)
                city = address.get('county', None)
                if not city:
                    # problem for New York City (osm_id=175905, osm_type=R)
                    city = address.get('state_district', None)
            country = address.get('country', None)
    return (lat, lon, city, country)
#===============================================================================
# TESTS
#===============================================================================
def test():
    lat, lon, city, country = location_for('Lyon', 'France')
    out = 'NOMINATIM result for location_for(Lyon, France)\n'+json.dumps({'lat': lat, 'lon': lon, 'city': city, 'country': country}, indent=4)
    print(out)
    lat, lon, city, country = reverse_location_for('15976890', 'way')
    out = 'NOMINATIM result for reverse_location_for(15976890, way)\n'+json.dumps({'lat': lat, 'lon': lon, 'city': city, 'country': country}, indent=4)
    print(out)
