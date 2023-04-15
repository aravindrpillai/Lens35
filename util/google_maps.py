import googlemaps 
from geopy.geocoders import GoogleV3
from geopy.distance import distance
from property_reader import PropertyReader

api_key = PropertyReader.get_property("google_maps","api_key")

def get_distance_bw_2_places(place_1, place_2):
    place_1 = 'Rosemala, 691309' 
    place_2 = 'HSR Layout, 560102'    
    gmaps = googlemaps.Client(key = api_key)  
    distance = gmaps.distance_matrix(place_1,place_2)['rows'][0]['elements'][0]
    return distance

def get_cordinates(address):
    geolocator = GoogleV3(api_key=api_key)
    location = geolocator.geocode(address)
    return (location.latitude, location.longitude)

def get_distance_bw_cordinates(cord_1, cord_2):
    #cord_1 = (8.930019099999999, 76.9064744)
    #cord_2 = (8.8137543, 76.7164246)
    return distance(cord_1, cord_2).km