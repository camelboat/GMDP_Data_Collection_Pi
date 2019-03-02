import serial
#import RPi.GPIO as GPIO
import time
#import re
import cv2

#import sys
#mport os

ser=serial.Serial("/dev/ttyACM0",9600)
ser.baudrate=9600
ser.timeout = 2

status = True

while True:
    try:
        read_ser=ser.readline()
        data_ser=read_ser.decode('utf-8')
        
        # temperature
        if data_ser[0]=="t":
            temperature = float(data_ser[1:])
            print("Temperature is ", temperature, "Celcius degree")

        # any_people, 0 for not detecting people, 1 for detecting people
        elif data_ser[0]=="p":
            any_people = int(data_ser[1:])
            if any_people == 0:
                print("There is no one in the room")
            else:
                print("There are someone in the room")

    except KeyboardInterrupt:
        break
