import inkyphat
from PIL import ImageFont
import national_rail_fetcher

inkyphat.set_colour("yellow")

font = ImageFont.truetype("./8bitoperator.ttf", 12)

print("Getting train services")

services = national_rail_fetcher.get_next_services()

print("Got upcoming train services")

some_services_delayed = any(x.etd != 'On time' for x in services)

lines = []
for service in services:
    time_string = service.std
    if(service.etd != 'On time'):
        time_string += ' ({expected})'.format(expected=service.etd)
    
    time_string_padded = '{time: <15}'.format(time=time_string) if some_services_delayed else '{time: <5}'.format(time=time_string)

    service_string = '{time} {destination} '.format(time=time_string_padded, destination=service.destination_text)

    lines.append(service_string)

y = 0
for line in lines:
    inkyphat.text((5, y), line, inkyphat.BLACK, font)
    y += 20

print("Displaying results")

inkyphat.show()

print("Finished")