import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
while True:
	GPIO.output(11,True)
	time.sleep(1)
	GPIO(11,False)
	time.sleep(1)
