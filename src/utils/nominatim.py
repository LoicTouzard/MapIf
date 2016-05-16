import requests
from urllib.parse import quote
import json

_BASE_URL_ = "http://nominatim.openstreetmap.org/search/"
_PARAMS_ = {
    'format': 'json',
    'addressdetails':'1',
    'limit':'1'
}

def location_for(city, country):
    url = _BASE_URL_ + quote('{city} {country}'.format(city=city, country=country))
    resp = requests.get(url, params=_PARAMS_)
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

# ------------------------------ TEST ZONE BELOW THIS LINE ---------------------------------

if __name__ == '__main__':
    lat, lon, city, country = location_for('Lyon', 'France')
    print(json.dumps({
            'lat': lat,
            'lon': lon,
            'city': city,
            'country': country
        }, indent=4))
