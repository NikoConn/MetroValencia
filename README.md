# MetroValencia

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

Python module that retrieves MetroValencia stations details and train's times for a given station.

Data from [Portal de datos abiertos del Ayuntamiento de València](https://valencia.opendatasoft.com) and [FGV](https://www.fgv.es).

# Installation

For installing this package in the latest release, just run the following command:

```
pip install "git+https://github.com/NikoConn/MetroValencia@$(curl -s https://api.github.com/repos/NikoConn/MetroValencia/releases/latest | grep '"tag_name":' | sed -E 's/.*\"([^\"]+)\".*/\1/')"
```

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
Retrieve plan to reach a destination:
```
import metrovalencia

# get plan to reach a destination
response = metrovalencia.get_plan(15, 39, fetch_available_trains=False)
print(response)
```
Output:
```
[
  {'station': {'id': 15, 'name': 'Colón', 'lines': [3, 5, 7, 9], 'location': [39.47014621855607, -0.3709277814305924]}, 'lines': [7]},
  {'station': {'id': 25, 'name': 'Jesús', 'lines': [1, 2, 7], 'location': [39.45920185236387, -0.38454166105416354]}, 'lines': [1]},
  {'station': {'id': 39, 'name': "L'Alcúdia", 'lines': [1], 'location': [39.193813363569774, -0.5102638606951693]}, 'lines': None}
]
```

# cli

The repo also includes a python cli with a working example

```
usage: MetroValencia [-h] [-l] [-c latitude,longitude] [-t stationid] [-p stationid,stationid]

This is a cli for using MetroValencia python API

optional arguments:
  -h, --help            show this help message and exit
  -l                    List stations
  -c latitude,longitude
                        Show closest station to coordinates in format latitude,longitude
  -t stationid          Id of the station to retrieve times
  -p stationid,stationid
                        Specify the transit station IDs for planning the route. Provide a comma-separated list of two station IDs, e.g.,
                        -p 123,456.
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
$ metrovalencia_cli -t 117
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

```
$ metrovalencia_cli -p 15,32
Take line 7 in Colón until Picanya
```
