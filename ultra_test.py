#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import json
import sys

try:
          space1, space2, spc, pulse_end_time_echo1, pulse_end_time_echo2 = 0, 0, 0, 0, 0

          GPIO.setmode(GPIO.BOARD)

          PIN_TRIGGER = 36
          PIN_ECHO1 = 31
          PIN_ECHO2 = 32
          
          GPIO.setup(PIN_TRIGGER, GPIO.OUT)
          GPIO.setup(PIN_ECHO1, GPIO.IN)
          GPIO.setup(PIN_ECHO2, GPIO.IN)

          GPIO.output(PIN_TRIGGER, GPIO.LOW)
          time.sleep(2)
          GPIO.output(PIN_TRIGGER, GPIO.HIGH)
          time.sleep(0.00001)
          GPIO.output(PIN_TRIGGER, GPIO.LOW)
          while GPIO.input(PIN_ECHO1) == 0:
                pulse_start_time_echo1 = time.time()
          while GPIO.input(PIN_ECHO1) == 1:
                pulse_end_time_echo1 = time.time()
          time.sleep(0.3)
          GPIO.output(PIN_TRIGGER, GPIO.HIGH)
          time.sleep(0.00001)
          GPIO.output(PIN_TRIGGER, GPIO.LOW)
          while GPIO.input(PIN_ECHO2) == 0:
                pulse_start_time_echo2 = time.time()
          while GPIO.input(PIN_ECHO2) == 1:
                pulse_end_time_echo2 = time.time()    
                
          pulse_duration1 = pulse_end_time_echo1 - pulse_start_time_echo1
          pulse_duration2 = pulse_end_time_echo2 - pulse_start_time_echo2
          distance1 = round(pulse_duration1 * 17150, 2)
          distance2 = round(pulse_duration2 * 17150, 2)
          #print distance1,distance2,distance3,distance4
          
          if distance1 >= 12:
                spc+=1 
                space1 = 1
          else:       
                space1 = 0
          if distance2 >= 12:
                spc+=1
                space2 = 1
          else:       
                space2 = 0

          print '{"Availibilty":"'+str(spc)+'", "Spots": "\\\"'+str(space1)+str(space2)+str(0)+str(0)+'\\\"" }'
finally: 
            GPIO.cleanup()
