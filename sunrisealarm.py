""" Sunrise alarm clock prototype """

import time
import random
import machine
import network
import ntptime

from stellar import StellarUnicorn
from picographics import PicoGraphics, DISPLAY_STELLAR_UNICORN as DISPLAY

try:
    from secrets import WIFI_SSID, WIFI_PASSWORD
    wifi_available = True
except ImportError:
    print("Create secrets.py with your WiFi credentials to get time from NTP")
    wifi_available = False

su = StellarUnicorn()
graphics = PicoGraphics(DISPLAY)

width = StellarUnicorn.WIDTH
height = StellarUnicorn.HEIGHT
print(f"width={width}, height={height}")

BRIGHTNESS_START=0.01
BRIGHTNESS_END=1.0
TIME_RAMP_S=1800 #1800 would be 30 mins
TIME_AFTER_S=600 #time to stay lit after sunrise
ALARM_TIME=(06,30) #hh:mm

def sync_time():
    """ Connect to wifi and synchronize the RTC time from NTP """
    if not wifi_available:
        return

    # Start connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    # Wait for connect success or failure
    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(0.2)

    if max_wait > 0:
        print("Connected")

        try:
            ntptime.settime()
            print("Time set")
        except OSError:
            pass

    wlan.disconnect()
    wlan.active(False)

def random_fill(r, g, b):
    """Fills a random pixel with the RGB colour"""
    graphics.set_pen(graphics.create_pen(int(r), int(g), int(b)))
    graphics.pixel(random.randint(0,width), random.randint(0,height))
                                
def clamp(n, min_value, max_value):
    """Clamps value to a range"""
    return max(min_value, min(n, max_value))

def brightness_ramp(time_diff):
    """Ramps brightness based on time since alarm"""
    print(f"time diff={time_diff}")
    brightness = ((BRIGHTNESS_END-BRIGHTNESS_START) * ((time_diff / TIME_RAMP_S))) + BRIGHTNESS_START
    brightness = clamp(brightness, BRIGHTNESS_START, BRIGHTNESS_END)
    print(f"brightness={brightness}")
    return brightness

def colour_shift(time_diff):
    """Picks a sky colour based on the time difference"""
    if time_diff < (TIME_RAMP_S * 0.2):
        return 0,17,131 #dark blue
    elif time_diff < (TIME_RAMP_S * 0.3):
        return 0,125,219 #brighter blue
    elif time_diff < (TIME_RAMP_S * 0.4):
        return 255,117,249 #pinkish
    elif time_diff < (TIME_RAMP_S * 0.5):
        return 255,117,117 #orange
    elif time_diff < (TIME_RAMP_S * 0.6):
        return 246,255,163 #pale yellow
    elif time_diff < (TIME_RAMP_S * 0.7):
        return 250,255,199 #paler yellow
    else:
        return 255,255,255 #white

def check_alarm(alarm_time):
    """Compares hours and mins of current timea against user alarm time"""
    local_time=time.localtime()
    if (ALARM_TIME[0]==local_time[3]) and (ALARM_TIME[1]==local_time[4]):
        return True
    else:
        return False

def sunrise_loop():
    """Run the sunrise ramp to completion"""
    time_diff_s = 0
    while time_diff_s < (TIME_RAMP_S+TIME_AFTER_S):
        now_time = time.ticks_ms()
        time_diff_s = time.ticks_diff(now_time, start_time) / 1000.0
        su.set_brightness(brightness_ramp(time_diff_s))
        colour = colour_shift(time_diff_s)
        random_fill(colour[0], colour[1], colour[2])
        su.update(graphics)
        time.sleep(0.1)

def initialise_display():
    # intialise all the things
    su.set_brightness(BRIGHTNESS_START)
    graphics.set_pen(graphics.create_pen(0, 0, 0))
    graphics.clear()
    su.update(graphics)

initialise_display()
sync_time()
print(f"UTC Time {time.gmtime()}")
print(f"Local Time {time.localtime()}")

while True:
    if check_alarm(ALARM_TIME):
        start_time = time.ticks_ms()
        sunrise_loop()
        initialise_display()
    time.sleep(1)