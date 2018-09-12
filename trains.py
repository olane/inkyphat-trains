import inkyphat
from PIL import ImageFont
import national_rail_fetcher
import time

inkyphat.set_colour("yellow")
font = ImageFont.truetype("./8bitoperator.ttf", 12)

UPDATE_PERIOD_SECONDS = 60*3
FONT_SIZE = 12
LINE_HEIGHT = 20
DELAY_TEXT_WIDTH = inkyphat.WIDTH // 4

def clear_area(start_x, start_y, width, height):
    for i in range(start_x, start_x + width):
        for j in range(start_y, start_y + height):
            inkyphat.putpixel((i, j), inkyphat.WHITE)

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
            clear_area(inkyphat.WIDTH - DELAY_TEXT_WIDTH, y, DELAY_TEXT_WIDTH, LINE_HEIGHT)
            estimated_time_string = ' ({expected})'.format(expected=service.etd)
            inkyphat.text((inkyphat.WIDTH - DELAY_TEXT_WIDTH, y), estimated_time_string, inkyphat.BLACK, font)
        
        y += LINE_HEIGHT

    inkyphat.show()
    print("Finished")

while True:
    update_display()
    time.sleep(UPDATE_PERIOD_SECONDS)
