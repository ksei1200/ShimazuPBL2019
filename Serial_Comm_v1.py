#Serial communication with QZ1

import serial
import sys
ser = serial.Serial('/dev/cu.usbserial-A7004NCE', 115200)
f = open('qzss.txt', 'ab')

for i in range(10000) :
    line = ser.readline()
    print(line)
    f.write(line)
    i =++1

ser.close()
f.close()
