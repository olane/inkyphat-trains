#!/usr/bin/python3.5

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
font_times_offset = -2
font_errors = font_times;

UPDATE_PERIOD_SECONDS = 90
UPDATE_PERIOD_AFTER_ERROR_SECONDS = 30
FONT_SIZE = 11
LINE_HEIGHT = inkyphat.HEIGHT // 5 + 1
LEFT_PADDING = 1
TIME_WIDTH = 43
DELAY_TEXT_WIDTH = inkyphat.WIDTH // 4
DELAY_TEXT_PADDING = 5

ROTATE_SCREEN = True

if(ROTATE_SCREEN):
    inkyphat.set_rotation(180)

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

    time_string_x = LEFT_PADDING
    time_string_y = y + font_services_offset
    destination_string_x = LEFT_PADDING + TIME_WIDTH
    destination_string_y = y + font_services_offset

    inkyphat.text((time_string_x, time_string_y), time_string, inkyphat.BLACK, font_services)
    inkyphat.text((destination_string_x, destination_string_y), destination_string, inkyphat.BLACK, font_services)

    cutout_start = inkyphat.WIDTH - DELAY_TEXT_WIDTH
    clear_area(cutout_start, y, DELAY_TEXT_WIDTH, LINE_HEIGHT)
    right_column_string_x = cutout_start + DELAY_TEXT_PADDING

    service_is_delayed = service.etd != 'On time'
    if(service_is_delayed):
        estimated_time_string = '({expected})'.format(expected=service.etd)
        inkyphat.text((right_column_string_x, y + font_times_offset), estimated_time_string, inkyphat.BLACK, font_times)

    try:
        text_offset = 10 if service_is_delayed else 0
        text_offset = text_offset + font_times_offset
        time_departure_delta_string = pretty_time_delta(service.time_until_departure.total_seconds())
        inkyphat.text((right_column_string_x, y + text_offset), time_departure_delta_string, inkyphat.YELLOW, font_times)
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
    try:
        update_display()
        time.sleep(UPDATE_PERIOD_SECONDS)
    except Exception as err:
        render_error(err)
        time.sleep(UPDATE_PERIOD_AFTER_ERROR_SECONDS)

def render_error(error):
    try:
        print("Error while updating display, attempting to render:", error)
        inkyphat.clear()
        inkyphat.set_border(inkyphat.WHITE)
        inkyphat.text((1, 1), repr(error), inkyphat.BLACK, font_errors)
    except Exception as error2:
        print("Exception while trying to render error:", error2)
