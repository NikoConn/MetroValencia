from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pytz

DATA_URL = 'https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/fgv-bocas/exports/json'
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
        - 'entrances': A list containing the geographical coordinates of different entrances to the station.
    """
    _stations = requests.get(DATA_URL).json()

    stations = {}
    for station in _stations:
        station_id = int(station['idparada'])
        
        if station_id not in stations.keys():
            stations[station_id] = {
                'id': station_id, 
                'name': station['denominacion'],
                'lines': [int(x) for x in station['lineas'].split(',')],
                'entrances': []
                }
        
        stations[station_id]['entrances'].append(station['geo_shape']['geometry']['coordinates'])

    return stations if id_indexed else list(stations.values())
