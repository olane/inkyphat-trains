import inkyphat
from PIL import ImageFont
import national_rail_fetcher
import time
import sys

station_from = sys.argv[1]
station_to = sys.argv[2]

inkyphat.set_colour("yellow")
font = ImageFont.truetype("./8bitoperator.ttf", 11)
small_font = ImageFont.truetype("./8bitoperator.ttf", 10)

UPDATE_PERIOD_SECONDS = 60*3
FONT_SIZE = 11
LINE_HEIGHT = inkyphat.HEIGHT // 5 + 1
LEFT_PADDING = 1
TIME_WIDTH = 43
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

        inkyphat.text((LEFT_PADDING, y-4), time_string, inkyphat.BLACK, font)
        inkyphat.text((LEFT_PADDING + TIME_WIDTH, y-4), destination_string, inkyphat.BLACK, font)

        if(service.etd != 'On time'):
            cutout_start = inkyphat.WIDTH - DELAY_TEXT_WIDTH
            text_start = cutout_start + DELAY_TEXT_PADDING

            clear_area(cutout_start, y, DELAY_TEXT_WIDTH, LINE_HEIGHT)
            estimated_time_string = '({expected})'.format(expected=service.etd)
            inkyphat.text((text_start, y), estimated_time_string, inkyphat.BLACK, font)

        time_departure_delta_string = pretty_time_delta(service.time_until_departure.total_seconds())
        inkyphat.text((LEFT_PADDING+TIME_WIDTH, y+7), time_departure_delta_string, inkyphat.YELLOW, small_font)
        
        y += LINE_HEIGHT

    inkyphat.show()
    print("Finished")

def pretty_time_delta(seconds):
    seconds = int(seconds)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if hours > 0:
        return '%dh%dm' % (hours, minutes)
    elif minutes > 0:
        return '%dm' % (minutes)
    else:
        return '%ds' % (seconds,)

while True:
    update_display()
    time.sleep(UPDATE_PERIOD_SECONDS)

