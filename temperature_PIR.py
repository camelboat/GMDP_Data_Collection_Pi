import serial
import time
import csv
import re
from datetime import datetime
import numpy as np
#import sys
#import cv2
#import RPi.GPIO as GPIO
import sys
from urllib.request import urlopen
import time
import statistics
#import os

ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = 9600
ser.timeout = 2
status = True
any_people = [0,0,0,0]

def get_time():
    return datetime.now().strftime("%H:%M:%S:%f")[:-3]

# Discard the first ten line data
# to avoid format problem
for i in range(1, 10):
    read_ser = ser.readline()

# count for uploading data
count = 0

baseURL = 'https://api.thingspeak.com/update?api_key=T9PJ3W9K7NSQ6AT8&field1=0'
upload_last = time.time()
data_list_temperature = []
data_list_PIR = []
data_list_PIR_1 = []
data_list_PIR_2 = []
data_list_PIR_3 = []
data_list_PIR_4 = []
data_list_PIR.append(data_list_PIR_1)
data_list_PIR.append(data_list_PIR_2)
data_list_PIR.append(data_list_PIR_3)
data_list_PIR.append(data_list_PIR_4)

while True:
    try:
        read_ser = ser.readline()
        #print(read_ser)

        data_ser = read_ser.decode('ISO-8859-1')
        #data_ser = read_ser.decode('utf-8')
        flag = data_ser[0]

        #print(flag)

        # temperature
        if flag == "t":
            now = get_time()
            print(now)
            temperature = float(data_ser[1:])
            print(temperature)
            #data_list[1].append(temperature)
            data_list_temperature.append(temperature)

        # PIR sensors
        else:
            any_people[int(flag)-1] = int(data_ser[1])
            print(any_people[int(flag)-1])
            data_list_PIR[int(flag)-1].append(any_people[int(flag)-1])

        # update data
        if time.time() - upload_last > 30:
            print("uploading")
            thingspeak = urlopen(baseURL + str(statistics.mean(data_list_temperature)))
            thingspeak.read()
            thingspeak.close()
            upload_last = time.time()
            print("Uploading finish")
            data_list_temperature.clear()
 
    except KeyboardInterrupt:
        # Write the whole data_list into data.csv
        with open('data.csv', mode='w') as output_file:
            output = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            output.writerows(zip(*data_list))
            #output.writerows(data_list)
        output_file.close()
        break


