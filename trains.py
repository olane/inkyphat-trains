import inkyphat
from PIL import ImageFont
import national_rail_fetcher
import time

inkyphat.set_colour("yellow")
font = ImageFont.truetype("./8bitoperator.ttf", 12)
update_period_seconds = 60*3

def clear_area(start_x, start_y, width, height):
    for i in range(start_x, start_x + width):
        for j in range(start_y, start_y + height):
            inkyphat.put_pixel((i, j), inkyphat.WHITE)

def update_display():
    print("Getting train services...")
    services = national_rail_fetcher.get_next_services()
    print("Got upcoming train services")

    print("Displaying results...")
    inkyphat.clear()
    y = 0
    for service in services:
        time_string = service.std
        destination_string = service.destination_text

        time_string_padded = '{time: <5}'.format(time=time_string)
        service_string = '{time} {destination} '.format(time=time_string_padded, destination=destination_string)

        inkyphat.text((5, y), service_string, inkyphat.BLACK, font)

        if(service.etd != 'On time'):
            clear_area(inkyphat.WIDTH - 40, y, 40, 20)
            estimated_time_string = ' ({expected})'.format(expected=service.etd)
            inkyphat.text((inkyphat.WIDTH - 40, y), estimated_time_string, inkyphat.BLACK, font)
        
        y += 20

    inkyphat.show()
    print("Finished")

while True:
    update_display()
    time.sleep(update_period_seconds)
