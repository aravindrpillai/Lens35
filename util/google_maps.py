import googlemaps 
# Requires API key 
gmaps = googlemaps.Client(key='secret_key')  
# Requires cities name 
distance = gmaps.distance_matrix('Rosemala, 691309','HSR Layout, 560102')['rows'][0]['elements'][0]

print(distance)