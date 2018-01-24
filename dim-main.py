#!/usr/local/bin/python

import RPi.GPIO as GPIO
import time
from datetime import datetime as dt

# 0 = Pressed
# Button starts script
# Hold for 3-5 seconds to shutdown

# Pins
button_pin = 22
mode_switch_button_pin = 18
ldr_pin = 7
red_sensor_led_pin = 15
blue_sleep_led_pin = 16
led_pin_1 = 33
led_pin_2 = 35
led_pin_3 = 37
led_pin_4 = 36
led_pin_5 = 38
led_pin_6 = 40

# Config
bed_time = 22
dim_time = bed_time - 1

# A Light-Dependent Resistor (LDR) is being used to charge a capacitor.
# The less light detected, the higher the resistance.
# Higher resistance = longer time to charge capacitor
def get_charge_time():
    charge_time = 0

    # Setup pin as output, & set output to low (zero-out the pin)
    GPIO.setup(ldr_pin, GPIO.OUT)
    GPIO.output(ldr_pin, GPIO.LOW)
    time.sleep(0.2)

    # Change the pin back to input
    GPIO.setup(ldr_pin, GPIO.IN)
  
    # Increment until the capacitor is charged
    while (GPIO.input(ldr_pin) == GPIO.LOW):
        charge_time += 1

    return charge_time

def disable_led(pin):
    GPIO.output(pin, False)

def disable_all_led():
    disable_led(led_pin_1)
    disable_led(led_pin_2)
    disable_led(led_pin_3)
    disable_led(led_pin_4)
    disable_led(led_pin_5)
    disable_led(led_pin_6)

def enable_led(pin):
    GPIO.output(pin, True)

def enable_all_led():
    enable_led(led_pin_1)
    enable_led(led_pin_2)
    enable_led(led_pin_3)
    enable_led(led_pin_4)
    enable_led(led_pin_5)
    enable_led(led_pin_6)

def setup_all_led():
    GPIO.setup(led_pin_1, GPIO.OUT)
    GPIO.setup(led_pin_2, GPIO.OUT)
    GPIO.setup(led_pin_3, GPIO.OUT)
    GPIO.setup(led_pin_4, GPIO.OUT)
    GPIO.setup(led_pin_5, GPIO.OUT)
    GPIO.setup(led_pin_6, GPIO.OUT)
    GPIO.setup(red_sensor_led_pin, GPIO.OUT)
    GPIO.setup(blue_sleep_led_pin, GPIO.OUT)

def get_ready_for_bed():
    if dt.now().minute == 10 and dt.now().second == 0:
        disable_led(led_pin_2)
        print '50 minutes until bedtime.'
    if dt.now().minute == 20 and dt.now().second == 0:
        disable_led(led_pin_3)
        print '40 minutes until bedtime.'
    if dt.now().minute == 30 and dt.now().second == 0:
        disable_led(led_pin_4)
        print '30 minutes until bedtime.'
    if dt.now().minute == 40 and dt.now().second == 0:
        disable_led(led_pin_5)
        print '20 minutes until bedtime.'
    if dt.now().minute == 50 and dt.now().second == 0:
        disable_led(led_pin_5)
        print '10 minutes until bedtime.'
    if dt.now().minute == 59 and dt.now().second == 0:
        disable_led(led_pin_6)
        print 'Goodnight sweet prince.'

def return_bed_time():
    if bed_time > 12:
        return str(bed_time - 12) + 'PM.'
    return str(bed_time) + 'AM.'


if __name__ == '__main__':
    system_started = False
    time_to_sleep = False
    first_print = False
    ignore_bedtime = False
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(button_pin, GPIO.IN)
        GPIO.setup(mode_switch_button_pin, GPIO.IN)
        setup_all_led()
        disable_all_led()
        
        while True:
            if GPIO.input(button_pin) == 0:
                print 'Light Sensor Mode has begun.'
                print 'Your bed time is currently set to: ' + return_bed_time()
                print 'The system will begin auto-dimming 1 hour prior.'
                system_started = True
                time.sleep(1)
                
            if not time_to_sleep and system_started:
                enable_led(red_sensor_led_pin)
                disable_led(blue_sleep_led_pin)
                
                if GPIO.input(mode_switch_button_pin) == 0:
                    if (dt.now().hour == dim_time and ignore_bedtime):
                        print 'Bed Time Mode has been resumed.'
                        time_to_sleep = True
                        ignore_bedtime = False
                        enable_all_led()
                        enable_led(blue_sleep_led_pin)
                        disable_led(red_sensor_led_pin)

                print get_charge_time()

                if get_charge_time() <= 430:
                    disable_all_led()

                if get_charge_time() in range(431, 860):
                    disable_led(led_pin_1)
                    disable_led(led_pin_2)
                    disable_led(led_pin_3)
                    disable_led(led_pin_4)
                    disable_led(led_pin_5)
                    enable_led(led_pin_6)

                if get_charge_time() in range(861, 1290):
                    disable_led(led_pin_1)
                    disable_led(led_pin_2)
                    disable_led(led_pin_3)
                    disable_led(led_pin_4)
                    enable_led(led_pin_5)
                    enable_led(led_pin_6)

                if get_charge_time() in range(1291, 1720):
                    disable_led(led_pin_1)
                    disable_led(led_pin_2)
                    disable_led(led_pin_3)
                    enable_led(led_pin_4)
                    enable_led(led_pin_5)
                    enable_led(led_pin_6)

                if get_charge_time() in range(1721, 2150):
                    disable_led(led_pin_1)
                    disable_led(led_pin_2)
                    enable_led(led_pin_3)
                    enable_led(led_pin_4)
                    enable_led(led_pin_5)
                    enable_led(led_pin_6)

                if get_charge_time() in range(2151, 2580):
                    disable_led(led_pin_1)
                    enable_led(led_pin_2)
                    enable_led(led_pin_3)
                    enable_led(led_pin_4)
                    enable_led(led_pin_5)
                    enable_led(led_pin_6)

                if get_charge_time() >= 2581:
                    enable_all_led()

            if system_started:
                if (dt.now().hour == dim_time and not ignore_bedtime):
                    if not first_print:
                        print 'Bed Time Mode has begun.'
                        enable_all_led()
                        enable_led(blue_sleep_led_pin)
                        disable_led(red_sensor_led_pin)
                        first_print = True
                    time_to_sleep = True
                    get_ready_for_bed()

                    if GPIO.input(mode_switch_button_pin) == 0:
                        print 'Bed Time Mode has been cancelled.'
                        time_to_sleep = False
                        first_print = False
                        ignore_bedtime = True

                if GPIO.input(button_pin) == 0:
                    print 'Shutting down..'
                    # disable_led(red_sensor_led_pin)
                    # disable_led(blue_sleep_led_pin)
                    # disable_all_led()
                    system_started = False
                    time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
