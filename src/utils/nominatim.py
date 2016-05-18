import requests
from urllib.parse import quote
import json

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
            country = address.get('country', None)
    return (lat, lon, city, country)

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

if __name__ == '__main__':
    lat, lon, city, country = location_for('Lyon', 'France')
    print(json.dumps({
            'lat': lat,
            'lon': lon,
            'city': city,
            'country': country
        }, indent=4))
    lat, lon, city, country = reverse_location_for('15976890', 'way')
    print(json.dumps({
            'lat': lat,
            'lon': lon,
            'city': city,
            'country': country
        }, indent=4))