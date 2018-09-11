from nredarwin.webservice import DarwinLdbSession
import secrets

darwin_sesh = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=secrets.api_key)

def get_next_services():
    station_from = 'CMB'
    station_to = 'ELY'

    board = darwin_sesh.get_station_board(station_from, destination_crs=station_to)
    services = board.train_services[0:5]

    return services
