# GMDP_Data_Collection_Pi

## Introduction
This program is running on raspberry pi, with an Arduino Uno connected to it through serial port. The repository for programs running on Arduino Uno is [here](https://github.com/camelboat/GMDP_Data_Collection_Arduino). The default port is /dev/ttyACM0.

Current setting of data reading interval is 100ms, which can be modified in the Arduino program, but cannot be changed by the instruction from pi in real time.

## Usage
Typical data transferred from Arduino Uno are:

```python
"t21.23\n" # for temperature
"p0\n"     # for PIR sensor
```

After decoding, these values would be stored in variables 

```python
float temperature # 21.23 (in Celcius degree)
int any_people    # 0 (0 for not detecting people, 1 for detecting people)
```
## Future Work
Since the function of counting people by camera using cv method currently doesn't work well enough, we are thinking about estimating the number of people by the combination of camera videos and PIR data. To do this, we may be going to add four or more PIR sensors in one room, and estimating the amount of people by counting the number of triggers. We are wondering if this computing process should be done on ThingSpeak or be done locally.
