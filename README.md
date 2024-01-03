# MetroValencia

[![PyPi Version](https://img.shields.io/pypi/v/MetroValencia.svg?color=forestgreen)](https://pypi.org/project/MetroValencia/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

Python module that retrieves MetroValencia stations details and train's times for a given station.

Data from [Portal de datos abiertos del Ayuntamiento de València](https://valencia.opendatasoft.com) and [Geoportal València](https://geoportal.valencia.es).

# Usage

Retrieve information about upcoming train arrivals at a specific station:
```
import metrovalencia

# get upcoming arrivals for stop 15
response = metrovalencia.get_arrivals(15)
print(response)
```
Output:
```
[
  {'line': 3, 'destination': 'Aeroport', 'arrival_time': 108},
  {'line': 5, 'destination': 'Marítim', 'arrival_time': 108},
  {'line': 5, 'destination': 'Marítim', 'arrival_time': 131},
  {'line': 3, 'destination': 'Aeroport', 'arrival_time': 159},
  {'line': 7, 'destination': 'Torrent Avinguda', 'arrival_time': 228},
  {'line': 7, 'destination': 'Torrent Avinguda', 'arrival_time': 258},
  {'line': 3, 'destination': 'Rafelbunyol', 'arrival_time': 468},
  {'line': 3, 'destination': 'Rafelbunyol', 'arrival_time': 474},
  {'line': 9, 'destination': 'Av. del Cid', 'arrival_time': 528},
  {'line': 3, 'destination': 'Av. del Cid', 'arrival_time': 569}
]
```
Retrieve information about train stations:
```
import metrovalencia

# get list of stations
response = metrovalencia.get_stations()
print(response)
```
Output:
```
[
  {'id': 117, 'name': 'QUART DE POBLET', 'lines': [3, 5, 9], 'entrances': [[-0.4418805544578805, 39.48108673046481]]},
  {'id': 200, 'name': 'FAITANAR', 'lines': [3, 5, 9], 'entrances': [[-0.4331833421365398, 39.47761917024598]]},
  ...
  {'id': 122, 'name': 'FRANCISCO CUBELLS', 'lines': [5, 6, 9], 'entrances': [[-0.33397299106717426, 39.463245390702866]]},
  {'id': 201, 'name': 'TORRE DEL VIRREY', 'lines': [1], 'entrances': [[-0.5419166679787194, 39.56866455016901]]}
]
```
Retrieve information about closest stations to given coordinates:
```
import metrovalencia

# get closest station to coordinates
response = metrovalencia.get_closest_stations([39.467520, -0.377058], n=2)
print(response)
```
Output:
```
[
  {'id': 16, 'name': 'XÀTIVA', 'lines': [3, 5, 9], 'entrances': [[39.46749135269451, -0.3759854820376232], [39.46783056273336, -0.3776404255345655], [39.467335133630534, -0.3767647684800705], [39.4672294497781, -0.37632536078820306]]}, 
  {'id': 51, 'name': 'PL. ESPANYA', 'lines': [1], 'entrances': [[39.46620247730024, -0.38157177623086064], [39.46574865099752, -0.3820898894124665]]}
]

```

# cli

The repo also includes a python cli with a working example

```
$ metrovalencia_cli.py -h
usage: MetroValencia [-h] [-l] [-c coordinates] [stationid]

This is a cli for using MetroValencia python API

positional arguments:
  stationid       Id of the station to retrieve times

options:
  -h, --help      show this help message and exit
  -l              List stations
  -c coordinates  Show closest station to coordinates in format latitude,longitude
```

```
$ metrovalencia_cli.py -l
Quart de poblet (117)
  Lines: [3, 5, 9]
  Entrances: [[-0.4418805544578805, 39.48108673046481]]

Faitanar (200)
  Lines: [3, 5, 9]
  Entrances: [[-0.4331833421365398, 39.47761917024598]]

  ...

Francisco cubells (122)
  Lines: [5, 6, 9]
  Entrances: [[-0.33397299106717426, 39.463245390702866]]

Torre del virrey (201)
  Lines: [1]
  Entrances: [[-0.5419166679787194, 39.56866455016901]]
```

```
$ metrovalencia_cli.py 117
Quart de poblet (117)
  Lines: [3, 5, 9]
  Entrances: [[-0.4418805544578805, 39.48108673046481]]
  Upcoming trains:
    3 - Aeroport - 02:59
    5 - Marítim - 02:59
    5 - Marítim - 03:13
    3 - Aeroport - 03:16
    3 - Rafelbunyol - 08:59
    3 - Rafelbunyol - 09:03
    5 - Aeroport - 12:59
    5 - Aeroport - 13:22
    9 - Alboraia Peris Aragó - 14:59
    9 - Alboraia Peris Aragó - 15:23
```

```
$ metrovalencia_cli -c 39.467520,-0.377058 
Xàtiva (16)
  Lines: [3, 5, 9]
  Entrances: [[39.46749135269451, -0.3759854820376232], [39.46783056273336, -0.3776404255345655], [39.467335133630534, -0.3767647684800705], [39.4672294497781, -0.37632536078820306]]
```
