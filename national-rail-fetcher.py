from nredarwin.webservice import DarwinLdbSession
import secrets

darwin_sesh = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=secrets.api_key)

station_from = 'CMB'
station_to = 'ELY'

board = darwin_sesh.get_station_board(station_from, destination_crs=station_to)
services = board.train_services[0:5]

some_services_delayed = any(x.etd != 'On time' for x in services)

# Loop through services
for service in services:
    time_string = service.std
    if(service.etd != 'On time'):
        time_string += ' ({expected})'.format(expected=service.etd)
    
    time_string_padded = '{time: <15}'.format(time=time_string) if some_services_delayed else '{time: <5}'.format(time=time_string)

    service_string = '{time} {destination: <12} '.format(time=time_string_padded, destination=service.destination_text)

    print(service_string)

