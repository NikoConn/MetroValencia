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

def get_plan(station1, station2, fetch_available_trains=True):
    """Retrieve a plan for traveling between two stations.

    This function calculates the optimal plan for traveling between two transit stations using a Breadth-First Search (BFS) approach. The plan includes a sequence of stations to visit and the corresponding lines to take.

    Args:
        station1 (int): The identifier of the starting station.
        station2 (int): The identifier of the destination station.
        fetch_available_trains (bool, optional): If True, considers available train lines for planning. This will cause the algorithm to take longer, but will ensure that the route is available. Defaults to True.

    Returns:
        list: A list of dictionaries representing the plan steps. Each dictionary includes:
        - 'station': A dictionary with details of the station in the step, including 'id', 'name', 'lines', and 'location'.
        - 'lines': A list of integers representing the lines to take at the station, applicable only when moving to the next station in the plan.
    """
    stations = get_stations(id_indexed=True)
    line_stations = {}
    stations_lines = {}
    for station in stations.values():
        lines = station['lines']
        if fetch_available_trains:
            lines = list(set([x['line'] for x in get_arrivals(station['id'])]))
        stations_lines[station['id']] = lines
        for line in lines:
            if line not in line_stations.keys():
                line_stations[line] = []
            line_stations[line].append(station)

    #BFS
    queue = [station1]
    visited = [station1]
    distances = {station1: 0}
    parents = {}

    while (len(queue) > 0):
        station_id = queue.pop(0)
        station = stations[station_id]

        adyacent_stations = [station for line in stations_lines[station['id']] for station in line_stations[line]]
        for adyacent_station in adyacent_stations:
            distance = distances[station_id] + get_distance(station['location'], adyacent_station['location'])

            if adyacent_station['id'] not in visited or distances[adyacent_station['id']] > distance:
                distances[adyacent_station['id']] = distance
                parents[adyacent_station['id']] = station_id
                queue.append(adyacent_station['id'])
                visited.append(adyacent_station['id'])

    # recreate path
    path = [station2]
    current_station = station2
    while parents[current_station] in parents:
        current_station = parents[current_station]
        path.append(current_station)
    path.append(station1)
    
    path = path[::-1]
    steps = []
    for index, station_id in enumerate(path):
        steps.append(
            {
                'station': stations[station_id],
                'lines': [x for x in stations_lines[station_id] if x in stations_lines[path[index+1]]] if index < len(path) - 1 else None,
            }
        )
    return steps

def get_plan_coordinates(coords1, coords2, fetch_available_trains=True):
    """Retrieve a plan for traveling between two sets of coordinates.

    This function calculates the optimal plan for traveling between two sets of coordinates, representing the starting and destination locations. The plan includes a sequence of transit stations to visit and the corresponding lines to take.

    Args:
        coords1 (tuple): A tuple representing the geographical coordinates (latitude, longitude) of the starting location.
        coords2 (tuple): A tuple representing the geographical coordinates (latitude, longitude) of the destination location.
        fetch_available_trains (bool, optional): If True, considers available train lines for planning. This will cause the algorithm to take longer, but will ensure that the route is available. Defaults to True.

    Returns:
        list: A list of dictionaries representing the plan steps. Each dictionary includes:
        - 'station': A dictionary with details of the transit station in the step, including 'id', 'name', 'lines', and 'location'.
        - 'lines': A list of integers representing the lines to take at the station, applicable only when moving to the next station in the plan.

    Note:
        The 'get_plan' function is then used to calculate the plan between the closest starting and destination stations.
    """
    initial_station = get_closest_stations(coords1, 1)[0]['id']
    final_station = get_closest_stations(coords2, 1)[0]['id']

    return get_plan(initial_station, final_station, fetch_available_trains=fetch_available_trains)
