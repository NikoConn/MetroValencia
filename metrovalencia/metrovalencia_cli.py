import metrovalencia
import argparse

def show_station(station):
    print('{} ({})'.format(station['name'].lower().capitalize(), station['id']))
    print('  Lines: {}'.format(station['lines']))
    print('  Entrances: {}'.format(station['entrances']))

def show_arrival(arrival):
    seconds = int(arrival['arrival_time'] % 60)
    minutes = int(arrival['arrival_time'] / 60)

    print('    {} - {} - {:02d}:{:02d}'.format(arrival['line'], arrival['destination'], minutes, seconds))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='MetroValencia',
        description='This is a cli for using MetroValencia python API',
    )

    parser.add_argument('-l', required=False, action='store_true', help='List stations')
    parser.add_argument('stationid', nargs='?', type=int, help='Id of the station to retrieve times')
    arguments = parser.parse_args()
    
    if(arguments.l):
        for x in metrovalencia.get_stations():
            show_station(x)
            print('')
    elif(arguments.stationid):
        stationid = arguments.stationid
        stations = metrovalencia.get_stations(id_indexed=True)

        if stationid not in stations.keys():
            parser.error('Invalid stationid.')
        station = stations[stationid]

        show_station(station)
        print('  Upcoming trains:')
        [show_arrival(x) for x in metrovalencia.get_arrivals(stationid)]
        
    else:
        parser.error("Positional argument stationid is required.")