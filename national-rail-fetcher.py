from nredarwin.webservice import DarwinLdbSession
import secrets

darwin_sesh = DarwinLdbSession(wsdl="https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx", api_key=secrets.api_key)

board = darwin_sesh.get_station_board('CMB', destination_crs='ELY')

print("\nNext departures for %s" % (board.location_name))
print("""
-------------------------------------------------------------------------------
|  PLAT  | DEST                                        |   SCHED   |    DUE   |
------------------------------------------------------------------------------- """)

# Loop through services
for service in board.train_services:
    print("| %6s | %43s | %9s | %8s |" %(service.platform or "", service.destination_text, service.std, service.etd))

# Print a footer 
print("-------------------------------------------------------------------------------")
