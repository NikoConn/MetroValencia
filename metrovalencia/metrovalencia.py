from bs4 import BeautifulSoup
from datetime import datetime
import requests
import math
import pytz

DATA_URL = 'https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/fgv-estacions-estaciones/exports/json?lang=es&timezone=Europe%2FBerlin'
ARRIVALS_URL = 'https://geoportal.valencia.es/geoportal-services/api/v1/salidas-metro.html?estacion={}'

def get_arrivals(station_id):
    """Retrieve information about upcoming train arrivals at a specific station.

    This function fetches data about the next train arrivals at a given station, including details such as line number, destination, and time until arrival.

    Args:
        station_id (int): The identifier of the station for which arrival information is to be fetched.

    Returns:
        list: A list of dictionaries containing details of upcoming train arrivals. Each dictionary includes:
        - 'line': The line number of the arriving train.
        - 'destination': The destination of the arriving train.
        - 'arrival_time': The time until arrival in seconds.
    """
    html = requests.get(ARRIVALS_URL.format(station_id)).text
    soup = BeautifulSoup(html, features="html.parser")

    _arrivals = soup.select('#page > div:nth-child(2) > div')
    arrivals = []
    for _arrival in _arrivals[1:]:
        line = int(_arrival.select_one('span:nth-child(2) > span:nth-child(1)').text.split('-')[0].strip())
        dest = _arrival.select_one('span:nth-child(2) > b').text

        now = datetime.now(pytz.country_timezones.get('Europe/Madrid'))
        arrival_time = datetime.now(pytz.country_timezones.get('Europe/Madrid'))

        arrival_time_text = _arrival.select_one('span:nth-child(2) > span:nth-child(4)').text
        hour, minute, second = [int(x) for x in arrival_time_text.split(':')]
        arrival_time = arrival_time.replace(hour=hour, minute=minute, second=second)

        if arrival_time < now:
            arrival_time = arrival_time + datetime.timedelta(days=1)

        arrival_time = arrival_time - now

        arrivals.append({
            'line': line, 
            'destination': dest, 
            'arrival_time': arrival_time.seconds
        })
    return arrivals

def get_stations(id_indexed=False):
    """Retrieve information about transit stations.

    This function fetches data about various transit stations, including their identifiers, names, associated lines, and geographical coordinates.

    Args:
        id_indexed (bool, optional): If True, returns a dictionary with station IDs as keys. If False, returns a list of station details. Defaults to False.

    Returns:
        dict or list: If id_indexed is True, a dictionary with station IDs as keys and their details as values. If id_indexed is False, a list of station details.

    Note:
        The station details include:
        - 'id': The unique identifier of the station.
        - 'name': The name of the station.
        - 'lines': A list of integers representing the lines associated with the station.
        - 'location': The geographical coordinates of the station.
    """
    _stations = requests.get(DATA_URL).json()

    stations = {}
    for station in _stations:
        station_id = int(station['codigo'])

        stations[station_id] = {
            'id': station_id, 
            'name': station['nombre'],
            'lines': [int(x) for x in station['linea'].split(',')],
            'location': station['geo_shape']['geometry']['coordinates'][::-1]
        }

    return stations if id_indexed else list(stations.values())

def get_distance(coord1, coord2):
    """Distance in meters between two coordinates

    Args:
        coord1 (list): lat,lon
        coord2 (list): lat,lon

    Returns:
        double: Distance in meters.
    """
    R = 6373.0

    lat1 = math.radians(coord1[0])
    lon1 = math.radians(coord1[1])
    lat2 = math.radians(coord2[0])
    lon2 = math.radians(coord2[1])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance * 1000

def get_closest_stations(coordinates, n=1):
    """Retrieve information about the closest transit stations to a given set of coordinates.

    Args:
        coordinates (tuple): A tuple representing the geographical coordinates (latitude, longitude) for which the closest stations are to be determined.
        n (int, optional): The number of closest stations to retrieve. Defaults to 1.

    Returns:
        list: A list of dictionaries containing details of the closest transit stations. Each dictionary includes:
        - 'id': The unique identifier of the station.
        - 'name': The name of the station.
        - 'lines': A list of integers representing the lines associated with the station.
        - 'location': The geographical coordinates of the station.
    """

    stations = get_stations(id_indexed=True)
    distances = {
        station_id: get_distance(station['location'], coordinates)
        for station_id, station in stations.items()
    }
    ordered_stations = sorted(distances.keys(), key=lambda x:distances[x])
    return [stations[station_id] for station_id in ordered_stations[:n]]

def get_plan(station1, station2):
    stations = get_stations(id_indexed=True)

    line_stations = {}
    for station in stations.values():
        lines = station['lines']
        for line in lines:
            if line not in line_stations.keys():
                line_stations[line] = []
            line_stations[line].append(station)

    #BFS
    queue = list(set([x['line'] for x in get_arrivals(stations[station1]['id'])]))
    visited = [x for x in queue]
    # queue = [*stations[station1]['lines']]
    # visited = [*stations[station1]['lines']]
    parents = {}

    target = [*stations[station2]['lines']]
    ending = -1
    while (len(queue) > 0):
        print(queue)
        print(line_stations)
        line = queue.pop(0)
        adyacents = line_stations[line]
        adyacents = [[y,x] for x in adyacents for y in x['lines'] if y not in visited]

        for adyacent, station in adyacents:
            if adyacent in visited:
                continue
            if line not in [x['line'] for x in get_arrivals(station['id'])]:
                continue
            visited.append(adyacent)
            parents[adyacent] = [station, line]
            queue.append(adyacent)

            if adyacent in target:
                ending = adyacent
                queue = []
                break

    camino = [[ending, stations[station2]]]

    while ending in parents.keys():
        ending = parents[ending][1]
        camino.append([ending, parents[ending][0] if ending in parents.keys() else stations[station1]])
    for [line, station] in camino[::-1]:
        print('Toma la linea {} en {}'.format(line, station['name']))
    
        
