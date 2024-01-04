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
  {'id': 95, 'name': 'Marxalenes', 'lines': [4], 'location': [39.48797229915813, -0.3838368950525468]}, 
  {'id': 55, 'name': 'Empalme', 'lines': [1, 2, 4], 'location': [39.499576608331175, -0.40210834198203727]}, 
  
  ...

  {'id': 101, 'name': 'La Granja', 'lines': [4], 'location': [39.50403217479327, -0.4124779998061252]}, 
  {'id': 102, 'name': 'Sant Joan', 'lines': [4], 'location': [39.50529102481966, -0.41632398912246604]}
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
  {'id': 16, 'name': 'Xàtiva', 'lines': [3, 5, 9], 'location': [39.46718601400712, -0.377375006091083]}, 
  {'id': 190, 'name': 'Alacant', 'lines': [10], 'location': [39.46472103939357, -0.37747700051225186]}
]

```

# cli

The repo also includes a python cli with a working example

```
$ metrovalencia_cli -h
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
$ metrovalencia_cli -l
Marxalenes (95)
  Lines: [4]
  Location: [39.48797229915813, -0.3838368950525468]

Empalme (55)
  Lines: [1, 2, 4]
  Location: [39.499576608331175, -0.40210834198203727]

  ...

Sant joan (102)
  Lines: [4]
  Location: [39.50529102481966, -0.41632398912246604]

Alacant (190)
  Lines: [10]
  Location: [39.46472103939357, -0.37747700051225186]
```

```
$ metrovalencia_cli 117
Quart de poblet (117)
  Lines: [3, 5, 9]
  Location: [39.48108677099763, -0.44188055413458743]
  Upcoming trains:
    3 - Aeroport - 00:09
    3 - Aeroport - 00:22
    3 - Aeroport - 03:09
    5 - Marítim - 03:09
    5 - Marítim - 03:23
    3 - Aeroport - 03:26
    3 - Rafelbunyol - 04:09
    3 - Rafelbunyol - 04:26
    3 - Rafelbunyol - 09:09
    3 - Rafelbunyol - 09:13
```

```
$ metrovalencia_cli -c 39.467520,-0.377058 
Xàtiva (16)
  Lines: [3, 5, 9]
  Entrances: [[39.46749135269451, -0.3759854820376232], [39.46783056273336, -0.3776404255345655], [39.467335133630534, -0.3767647684800705], [39.4672294497781, -0.37632536078820306]]
```
