import serial
import time

#import cv2
#import RPi.GPIO as GPIO
#import re
#import sys
#mport os

ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = 9600
ser.timeout = 2
status = True
any_people = [0,0,0,0]

delay = 100 # ms
interval = 5 # s
read_num = interval * 1000 / delay * 4 # This is not very accurate 
count = 0
trigger = 0

# Discard the first ten line data
# to avoid format problem
for i in range(1, 10):
    read_ser = ser.readline()

while True:
    try:
        read_ser = ser.readline()
        #print(read_ser)

        data_ser = read_ser.decode('utf-8')
        flag = data_ser[0]
        #print(flag)

        # temperature
        if flag == "t":
            temperature = float(data_ser[1:])
            #print("Temperature is %f Celcius degree" % temperature)
            #print(temperature)

        # PIR sensors
        else:
            any_people[int(flag)-1] = int(data_ser[1])
            #print(any_people[int(flag)-1])

            count+=1
            if any_people[int(flag)-1] == 1:
                trigger+=1
            if count == read_num:
                print("In last %d s, PIR sensors have been triggered for %d times" % (interval, trigger))
                count = 0
                trigger = 0

    except KeyboardInterrupt:
        break
