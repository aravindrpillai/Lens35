import googlemaps 
# Requires API key 
gmaps = googlemaps.Client(key='AIzaSyAxDro6aI_GmBD8bJo0M16EVXuYm8WtbhA')  
# Requires cities name 
distance = gmaps.distance_matrix('Rosemala, 691309','HSR Layout, 560102')['rows'][0]['elements'][0]

print(distance)