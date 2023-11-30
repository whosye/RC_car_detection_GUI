import time
import random
import threading
import pygame
import os
import serial 
import sounddevice as sd
import soundfile as sf


import serial



"""
while True:
    
    i = input("input (on/off): ").strip()
    
    ser.write(i.encode())
    time.sleep(0.5)
    print(ser.readline().decode('ascii'))
"""

"""
ser = serial.Serial('COM4', 9600); 
ser.timeout = 1 
var = 'on'
varoff = 'off'
while True:
    
    ser.write(var.encode())
    ll  = ser.readline().decode('ascii')
    time.sleep(1)
    ser.write(varoff.encode())
    ll  = ser.readline().decode('ascii')
    print(ll)
    time.sleep(1)

"""
    

import serial
import time

def ToggleLeds(var):
    try:
        ser = serial.Serial('COM4', 9600)
        ser.timeout = 1

        for _ in range(2):
            ser.write(var.encode())
            ll = ser.readline().decode('ascii')
            time.sleep(3)
            print(ll)

            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if ser.is_open:
            ser.close()



while True:
    i = input("write").strip()
    print(i)
    time.sleep(3)
    ToggleLeds(i)