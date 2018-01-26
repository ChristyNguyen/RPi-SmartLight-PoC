# RPi SmartLight PoC

This was the software written for a school group project that required the use of a Raspberry Pi.
Project date: April 17, 2017

## Overview

We wanted to use the Raspberry Pi as a smart home light controller so that lights in one’s home will operate at the appropriate level of brightness. During the evening, the home’s lights will be set to a lower brightness in order to encourage the occupants to go to sleep.

With a few modifications to our original plan, we were able to demonstrate a similar concept on a small-scale level. We gave our project two modes: Light Sensor Mode and Bed Time Mode. In Light Sensor Mode, the LEDs dim accordingly depending on the amount of light that the photoresistor detects. Bed Time Mode begins one hour prior to the hour that is configured in the code (and in the case of the demonstration, 30 seconds before the minute that is configured in the code). During this mode, the lights begin dimming at set intervals until the specified bedtime.

![pin layout](https://github.com/ChristyNguyen/RPi-SmartLight-PoC/blob/master/layout.PNG)
