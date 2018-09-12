import inkyphat
from PIL import ImageFont
import national_rail_fetcher
import time
import sys

station_from = sys.argv[1]
station_to = sys.argv[2]

inkyphat.set_colour("yellow")
font = ImageFont.truetype("./8bitoperator.ttf", 12)

UPDATE_PERIOD_SECONDS = 60*3
FONT_SIZE = 12
LINE_HEIGHT = 20
LEFT_PADDING = 1
TIME_WIDTH = 45
DELAY_TEXT_WIDTH = inkyphat.WIDTH // 4
DELAY_TEXT_PADDING = 5

def clear_area(start_x, start_y, width, height):
    for i in range(start_x, start_x + width):
        for j in range(start_y, start_y + height):
            inkyphat.putpixel((i, j), inkyphat.WHITE)

def update_display():
    print("Getting train services...")
    services = national_rail_fetcher.get_next_services(station_from, station_to)
    print("Got upcoming train services")

    print("Displaying results...")
    inkyphat.clear()
    inkyphat.set_border(inkyphat.WHITE)
    y = 0
    for service in services:
        time_string = service.std
        destination_string = service.destination_text

        inkyphat.text((LEFT_PADDING, y), time_string, inkyphat.BLACK, font)
        inkyphat.text((LEFT_PADDING + TIME_WIDTH, y), destination_string, inkyphat.BLACK, font)

        if(service.etd != 'On time'):
            cutout_start = inkyphat.WIDTH - DELAY_TEXT_WIDTH
            text_start = cutout_start + DELAY_TEXT_PADDING

            clear_area(cutout_start, y, DELAY_TEXT_WIDTH, LINE_HEIGHT)
            estimated_time_string = '({expected})'.format(expected=service.etd)
            inkyphat.text((text_start, y), estimated_time_string, inkyphat.BLACK, font)
        
        y += LINE_HEIGHT

    inkyphat.show()
    print("Finished")

while True:
    update_display()
    time.sleep(UPDATE_PERIOD_SECONDS)
