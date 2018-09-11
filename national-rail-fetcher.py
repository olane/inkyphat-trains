from nredarwin.webservice import DarwinLdbSession
import secrets

darwin_sesh = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=secrets.api_key)

board = darwin_sesh.get_station_board('MAN')

print(board.location_name)