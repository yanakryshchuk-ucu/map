import folium
import pandas

from geopy.geocoders import GoogleV3
from geopy.extra.rate_limiter import RateLimiter


MAX_MOVIES = 30 # set max processed movies

geolocator = GoogleV3(api_key="AIzaSyB20jGkWeUIOqGJ9isjrRuOJp2CoXGB5JU", timeout=5)
#    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
geocache = {}

layer_fill_colors = {
    "A": "green",
    "B": "blue",
    "C": "yellow",
    "D": "orange",
    "E": "magenta",
    "F": "brown",
    "G": "white",
    "H": "red",
    "I": "purple",
    "J": "pink",
    "K": "darkblue",
    "L": "lightblue",
    "M": "lightgreen",
    "N": "darkgreen",
    "O": "orange",
    "P": "lightred",
    "Q": "darkpurple",
    "R": "maroon",
    "S": "olive",
    "T": "aqua",
    "U": "teal",
    "V": "navy",
    "W": "lime",
    "X": "fuchsia",
    "Y": "salmon",
    "Z": "indigo",

}


def read_year():
    """
    Return year from user's input
    """
    try:
        year = int(input("Enter year: "))
        return  year
    except:
        print("Invalid input! Enter year!")
        exit(-1)


def get_movies_data(filename, testyear):
    """
    (str, int)-> list
    Returns list each element of which is a tuple with movie name,add info and location.
    """
    lst = []
    hashes = set()
    data = pandas.read_csv(filename, error_bad_lines=False)
    for movie,year, add_info, location in zip(data['movie'],data['year'], data['add_info'], data['location']):
        if len(lst) >= MAX_MOVIES:
            return lst
        if year != 'NO DATA':
            try:
                if '/' in year:
                    movieyear = int(year[:4]) # in case of quarter in data
                else:
                    movieyear = int(year)
            except:
                movieyear = -1
                print("Invalid year in row", year)
            if movieyear == testyear:
                hash = year + movie + location  # year, name and location of movie
                if hash not in hashes:
                    loc = get_location(location)
                    if loc != None:
                        lst.append((movie, add_info, get_location(location)))
                    hashes.add(hash)
    return lst


def get_location(location_str):
    """
    Converts data with adress to coordinates and returns location
    """
    if location_str in geocache:
        return  geocache[location_str]
    else:
        print("resolving location of", location_str)
        location = geolocator.geocode(location_str)
        geocache[location_str] = location
        return  location


def create_map_with_layers(movies):
    """
    Create and return a map with multiple layers
    """
    map = folium.Map(tiles="OpenStreetMap")
    layers = {}
    for movie in movies:
        lid, layer_ = layer(movie[0], layers) # lid - layer id
        layer_.add_child(folium.CircleMarker(location=[movie[2].latitude, movie[2].longitude],
                                            radius=7,
                                            popup= movie[0] + "\n" + movie[1],
                                            fill_color= fill_colour_of_layer(lid),
                                            color = 'white',
                                            fill_opacity= 0.75))
    for layer_id in layers:
        map.add_child(layers[layer_id])
    map.add_child(folium.LayerControl())
    return map


def fill_colour_of_layer(layer_id):
    """
    Returns the colour which will fill the marker on defined layer
    """
    if layer_id in layer_fill_colors:
        return layer_fill_colors[layer_id]
    else:
        return 'grey'


def layer(moviename, layers):
    """
    Create layers
    """
    first = moviename[0].upper()
    if 'A' <= first <= 'Z':
        id = first
    else:
        id = 'other'
    if id in layers:
        return id, layers[id]
    else:
        layer = folium.FeatureGroup(name = id)
        layers[id] = layer
        return  id, layer


if __name__ == '__main__':
    year = read_year()
    movielist = get_movies_data('locations.csv', year)
    map = create_map_with_layers(movielist)
    map.save('Movies.html')


