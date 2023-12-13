import serial 
import serial.tools.list_ports
from time import time, sleep
import pygame
import os 
def WritoToArduino(num,ser):
    # Accepts only nums = [1, 2, 3, 4, 5]
    if num in ['1', '2', '3', '4', '5']:
        command = num
        print(f"Command sent: {command}")
        ser.write(command.encode())
    else:
        print("Invalid input. Accepted values are '1', '2', '3', '4', or '5'.")
    
"""    
def ToggleLeds():
    global ThirdLayer 
    try:
        ser = serial.Serial('COM4', 9600); 
        ser.timeout = 1 
        var = 'on'
        while True:
                if ThirdLayer == False:
                ser.write(var.encode())
                time.sleep(0.5)
                ll  = ser.readline().decode('ascii')
                print(ll)
                if ll == 'Led on':
                    print("DONE")
                    break
    except:
        return
        """