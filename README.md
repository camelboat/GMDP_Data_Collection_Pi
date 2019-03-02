# GMDP_Data_Collection_Pi

## Introduction
This program is running on raspberry pi, with an Arduino Uno connected to it through serial port
The default port is /dev/ttyACM0

Current setting of data reading interval is 100ms, which can be modified in the Arduino program, but cannot be changed by the instruction from pi in real time

## Usage
Typical data transferred from Arduino Uno are:

```python
"t21.23\n" # for temperature
"p0\n" # for PIR sensor
```

After decoding, these values would be stored in variables 

```python
float temperature #21.23
int any_people #0
```

