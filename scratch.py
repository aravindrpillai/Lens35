from math import radians, sin, cos, sqrt, atan2
from geopy.distance import distance
import time

def get_distance_using_haversine_formula(cord_1, cord_2):
    lat1 = cord_1[0]
    lon1 = cord_1[1]
    lat2 = cord_2[0]
    lon2 = cord_2[1]
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(radians, [lat1, lon1, lat2, lon2])
    R = 3958.8 # Earth's radius in miles
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance_km = R * c * 1.60934
    return distance_km

l1 = (8.930019099999999, 76.9064744)
l2 = (8.8137543, 76.7164246)

start_time = time.time()
distance_using_haversine =  get_distance_using_haversine_formula(l1, l2)
end_time = time.time()
elapsed_time = end_time - start_time
print("1. Elapsed time: ", elapsed_time, "seconds")

start_time = time.time()
distance_using_google = distance(l1, l2).km
end_time = time.time()
elapsed_time = end_time - start_time
print("2. Elapsed time: ", elapsed_time, "seconds")


print("Haversine : {} | Google : {}".format(distance_using_haversine, distance_using_google))


import configparser

class PropertyReader:
    @staticmethod
    def get_property(section, key):
        config = configparser.ConfigParser()
        config.read("C:/lens_35.properties")
        try:
            return config.get(section, key)
        except configparser.NoOptionError:
            return None


print(PropertyReader.get_property("google_maps", "api_key"))