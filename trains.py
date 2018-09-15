import inkyphat
from PIL import ImageFont
import national_rail_fetcher
import time
import sys

station_from = sys.argv[1]
station_to = sys.argv[2]

inkyphat.set_colour("yellow")
font_services = ImageFont.truetype("./8bitoperator.ttf", 11)
font_services_offset = -4
font_times = ImageFont.truetype("./8bitoperator.ttf", 10)
font_times_offset = -3

UPDATE_PERIOD_SECONDS = 60*3
FONT_SIZE = 11
LINE_HEIGHT = inkyphat.HEIGHT // 5 + 1
LEFT_PADDING = 1
TIME_WIDTH = 43
DELAY_TEXT_WIDTH = inkyphat.WIDTH // 4
DELAY_TEXT_PADDING = 5

def clear_area(start_x, start_y, width, height):
    x = max(start_x, 0)
    y = max(start_y, 0)
    x_end = min(start_x + width, inkyphat.WIDTH - 1)
    y_end = min(start_y + height, inkyphat.HEIGHT - 1)
    
    for i in range(x, x_end):
        for j in range(y, y_end):
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
        render_service(service, y)
        y += LINE_HEIGHT

    inkyphat.show()
    print("Finished")

def render_service(service, y):
    time_string = service.std
    destination_string = service.destination_text

    inkyphat.text((LEFT_PADDING, y + font_services_offset), time_string, inkyphat.BLACK, font_services)
    inkyphat.text((LEFT_PADDING + TIME_WIDTH, y + font_services_offset), destination_string, inkyphat.BLACK, font_services)

    cutout_start = inkyphat.WIDTH - DELAY_TEXT_WIDTH
    text_start = cutout_start + DELAY_TEXT_PADDING
    clear_area(cutout_start, y, DELAY_TEXT_WIDTH, LINE_HEIGHT)

    service_is_delayed = service.etd != 'On time'
    if(service_is_delayed):
        estimated_time_string = '({expected})'.format(expected=service.etd)
        inkyphat.text((text_start, y + font_times_offset), estimated_time_string, inkyphat.BLACK, font_times)

    try:
        text_offset = 10 if service_is_delayed else 0
        text_offset = text_offset + font_times_offset
        time_departure_delta_string = pretty_time_delta(service.time_until_departure.total_seconds())
        inkyphat.text((text_start, text_offset), time_departure_delta_string, inkyphat.YELLOW, font_times)
    except AttributeError:
        pass
        # there was no time until departure, presumably

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

