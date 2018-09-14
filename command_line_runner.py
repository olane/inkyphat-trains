import national_rail_fetcher
import sys

station_from = sys.argv[1]
station_to = sys.argv[2]
services = national_rail_fetcher.get_next_services(station_from, station_to)

some_services_delayed = any(x.etd != 'On time' for x in services)

lines = []
for service in services:
    time_string = service.std
    if(service.etd != 'On time'):
        time_string += ' ({expected})'.format(expected=service.etd)
    
    time_string_padded = '{time: <15}'.format(time=time_string) if some_services_delayed else '{time: <5}'.format(time=time_string)

    service_string = '{time} {destination} '.format(time=time_string_padded, destination=service.destination_text)

    lines.append(service_string)

for line in lines:
    print(line)