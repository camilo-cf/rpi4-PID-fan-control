#!/usr/bin/python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys
import numpy as np

# Configuration
FAN_PIN = 12  # BCM pin used to drive transistor's base
WAIT_TIME = 1  # [s] Time to wait between each refresh
FAN_MIN = 30  # [%] Fan minimum speed.
PWM_FREQ = 25  # [Hz] Change this value if fan has strange behavior

# Setup GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
fan.start(100)

# Fan PID
T_reference = 45
T_max = 65
T_min = 40
Kp = 5
Ki = 0.2
Kd = 1
dt = WAIT_TIME


# Fucntions
def get_temperature():
    """Function to read CPU temperature"""
    cpuTempFile = open("/sys/class/thermal/thermal_zone0/temp", "r")
    cpuTemp = float(cpuTempFile.read()) / 1000
    cpuTempFile.close()
    return cpuTemp

# PID constants and control variables
error = 0
error_prev = 0
temp = 0
temp_prev = 0
i_error = 0


try:
    while True:
        # Read CPU temperature
        temp = get_temperature()

        # Temperature under the limit
        if temp < T_min:
            C = 0

        # Temperature over the limit
        elif temp > T_max :
            C = 100

        # Temperature in range
        else:
            error = temp-T_reference

            # calculate the integral error
            i_error = i_error + (Ki * error * dt)
            # calculate the measurement derivative
            dpv = (temp - temp_prev) / dt
            # calculate the PID output
            P = Kp * error
            I = i_error
            D = -Kd * dpv
            #print("Control: ", P+I+D)
            #print("P: ",P)
            #print("I: ",I)
            #print("D: ",D)
            C = np.clip(P + I + D, FAN_MIN, 100)


        temp_prev = temp
        #print("error :",error)
        #print("C :",C)
        
        # Update fan speed
        fan.ChangeDutyCycle(C)

        # Wait until next refresh
        time.sleep(WAIT_TIME)


# If a keyboard interrupt occurs (ctrl + c), the GPIO is set to 0 and the program exits.
except KeyboardInterrupt:
    print("Fan ctrl interrupted by keyboard")
    GPIO.cleanup()
    sys.exit()
                      
            
