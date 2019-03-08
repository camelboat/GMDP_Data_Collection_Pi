import sys
from time import sleep
from urllib.request import urlopen

baseURL = 'https://api.thingspeak.com/update?api_key=T9PJ3W9K7NSQ6AT8&field1=0'

a=0
b=1
c=0

while(a < 1000):
    f = urlopen(baseURL + str(a))
    f.read()
    f.close()
    sleep(5)
    c = a
    a = a+b
    b = c
print(over)


