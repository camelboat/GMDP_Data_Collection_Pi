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
#mport os

ser = serial.Serial("/dev/ttyACM0",9600)
ser.baudrate = 9600
ser.timeout = 2
status = True
any_people = [0,0,0,0]

#delay = 100 # ms
#interval = 5 # s
#read_num = interval * 1000 / delay * 4 # This is not very accurate 
#count = 0
#trigger = 0

data_list = [['Time'],['Temperature'],['PIR_1'],['PIR_2'],['PIR_3'],['PIR_4']]

def get_time():
    return datetime.now().strftime("%H:%M:%S:%f")[:-3]

def add_time():
    data_list[0].append(get_time())

# Discard the first ten line data
# to avoid format problem
for i in range(1, 10):
    read_ser = ser.readline()

# count for uploading data
count = 0

baseURL = 'https://api.thingspeak.com/update?api_key=T9PJ3W9K7NSQ6AT8&field1=0'

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
            data_list[0].append(now)
            #add_time()

            temperature = float(data_ser[1:])
            #print("Temperature is %f Celcius degree" % temperature)
            #print(temperature)
            data_list[1].append(temperature)
            count+=1
            if count == 10:
                print("Uploading")
                thingspeak = urlopen(baseURL + str(temperature))
                thingspeak.read()
                thingspeak.close()
                print("Uploading finish")
                count = 0

        # PIR sensors
        else:
            any_people[int(flag)-1] = int(data_ser[1])
            #print(any_people[int(flag)-1])
            data_list[int(flag)+1].append(any_people[int(flag)-1])

            #count+=1
            #if any_people[int(flag)-1] == 1:
            #    trigger+=1
            #if count == read_num:
            #    print("In last %d s, PIR sensors have been triggered for %d times" % (interval, trigger))
            #    count = 0
            #    trigger = 0

    except KeyboardInterrupt:
        # Write the whole data_list into data.csv
        with open('data.csv', mode='w') as output_file:
            output = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            output.writerows(zip(*data_list))
            #output.writerows(data_list)
        output_file.close()
        break


