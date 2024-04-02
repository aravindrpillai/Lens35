import googlemaps 
from geopy.geocoders import GoogleV3
from geopy.distance import distance
from util.property_reader import PropertyReader

#Set this to true for testing purpose
DISABLE_GMAPS = True 

import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_distance_bw_2_places(place_1, place_2):
    if(DISABLE_GMAPS):
        return 4
    else:
        api_key = PropertyReader.get_property("google_maps","api_key")
        place_1 = 'Rosemala, 691309' 
        place_2 = 'HSR Layout, 560102'    
        gmaps = googlemaps.Client(key = api_key, ssl_context=ctx)  
        distance = gmaps.distance_matrix(place_1,place_2)['rows'][0]['elements'][0]
        return distance

def get_cordinates(address):
    if(DISABLE_GMAPS):
        return (100.000, 100.000)
    else:
        api_key = PropertyReader.get_property("google_maps","api_key")
        geolocator = GoogleV3(api_key=api_key, ssl_context=ctx)
        location = geolocator.geocode(address)
        return (location.latitude, location.longitude)
    
def get_distance_bw_cordinates(cord_1, cord_2):
    if(DISABLE_GMAPS):
        return 2
    else:
        return distance(cord_1, cord_2).km