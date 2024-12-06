Sunrise alarm clock based on [Pimoroni Stellar Unicorn](https://shop.pimoroni.com/products/space-unicorns?variant=40842632953939).  The basic concept is to simulate a sunrise using an LED panel.  The LEDs get brighter and shift in colour over a period of time.

Settings are all hard-coded.  You can tweak the alarm time, the ramp time, etc

```python
BRIGHTNESS_START=0.01
BRIGHTNESS_END=1.0
TIME_RAMP_S=1800 #1800 is 30 mins
TIME_AFTER_S=600 #time to stay lit after sunrise
ALARM_TIME=(06,30) #hh:mm
```

You will need to add your WIFI settings to a file called secrets.py
```python
WIFI_SSID = "Your WiFi SSID"
WIFI_PASSWORD = "Your WiFi password"
```
Copy both files to your Stellar Unicorn.  The simplest way is to use [Thonny](https://thonny.org).  General guidance on using MicroPython with the Pico is [here](https://learn.pimoroni.com/article/getting-started-with-pico)
