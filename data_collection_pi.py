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
import requests
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

baseURL_temperature = 'https://api.thingspeak.com/update?api_key=T9PJ3W9K7NSQ6AT8&field1=0'
baseURL_PIR = 'https://api.thingspeak.com/update?api_key=T9PJ3W9K7NSQ6AT8&field2=0'
upload_last = time.time()
upload_temperature_status = 0
upload_PIR_status = 0
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

def upload_data(baseURL, data):
    print('uploading')
    thingspeak = requests.get(baseURL + str(data))
    print(thingspeak.content)
    print('upload finish')

while True:
    try:
        read_ser = ser.readline()
        data_ser = read_ser.decode('ISO-8859-1')
        #data_ser = read_ser.decode('utf-8')
        flag = data_ser[0]

        #print(flag)

        # temperature
        if flag == "t":
            print(get_time())
            temperature = float(data_ser[1:])
            #print(temperature)
            data_list_temperature.append(temperature)
 
        # PIR sensors
        else:
            any_people[int(flag)-1] = int(data_ser[1])
            #print(any_people[int(flag)-1])
            data_list_PIR[int(flag)-1].append(any_people[int(flag)-1])

        # update data
        if (time.time() - upload_last > 15) and (time.time() - upload_last < 30) and (upload_temperature_status == 0):
            print('upload temperature')
            upload_data(baseURL_temperature, statistics.mean(data_list_temperature))
            upload_temperature_status = 1
            upload_PIR_status = 0
            data_list_temperature.clear()
        elif (time.time() - upload_last >= 30) and (upload_PIR_status == 0):
            print('upload_PIR')
            trigger_sum = 0
            for i in range(0, 3):
                trigger_sum += sum(data_list_PIR[i])
                print('add' + str(data_list_PIR[i]))
                data_list_PIR[i].clear()
            upload_data(baseURL_PIR, trigger_sum)
            upload_PIR_status = 1
            upload_temperature_status = 0
            upload_last = time.time()


    except KeyboardInterrupt:
        break


