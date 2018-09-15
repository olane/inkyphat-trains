from nredarwin.webservice import DarwinLdbSession
import secrets
from datetime import datetime, time, date, timedelta

darwin_sesh = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=secrets.api_key)

def get_next_services(station_from, station_to):
    board = darwin_sesh.get_station_board(station_from, destination_crs=station_to)
    services = board.train_services[0:5]

    for service in services:
        attach_time_until_departure(service)

    return services

def attach_time_until_departure(service):
    try:
        time_of_departure = get_time_of_departure(service)
        datetime_of_departure = get_datetime_from_board_time(time_of_departure)
        service.time_until_departure = datetime_of_departure - datetime.now()
    except:
        pass
        # Don't care if we fail to attach time until departure

# Note: this assumes that the time it is passed is
#    - less than 1 hour in the past
#    - less than 23 hours in the future
def get_datetime_from_board_time(board_time):
    time_portion = datetime.strptime(board_time,"%H:%M")
    d = datetime.combine(datetime.today(), time_portion.time())

    if d < (datetime.now() - timedelta(hours=1)):
        # The time we parsed was past midnight, so we should combine it with tomorrow's date not today's
        d = d + timedelta(days=1)

    return d

def get_time_of_departure(service):
    time_of_departure = service.etd 
    if(time_of_departure == 'On time'):
        time_of_departure = service.std 
    return time_of_departure