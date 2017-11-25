# This is the main Aquarium Controller script
# Nick Barsley, Feb 2017

import time
import urllib2							# Used to call Seneye API to get my reef values
import Adafruit_GPIO
from time import gmtime, strftime
from datetime import datetime
import RPi.GPIO as GPIO
import Adafruit_CharLCD as LCD
#from watchdogdev import *


###################################################################
# Set up hardware on Raspberry Pi

# Set up watchdog feeder
#~ wdt = watchdog('/dev/watchdog')
#~ try:
	#~ wdt.settimeout(15)
	#~ timeout = wdt.get_timeout()
	#~ print timeout,
	#~ print ' sec  --> changing timeout was successful'
#~ except IOError, e:
	#~ print e

# Set up LCD screen library
lcd = LCD.Adafruit_CharLCDPlate()
lcd.clear()

# Plus anything to do with the five keys on the LCD screen?
GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN)				# 3 pins for leak sensors - can I be more efficient and use just one pin as an 'Or'?)
GPIO.setup(24, GPIO.IN)
GPIO.setup(25, GPIO.IN)

# Feed button sensor
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Motor controls
GPIO.setup(05, GPIO.OUT)				# Output to control the RETURN PUMP
GPIO.setup(06, GPIO.OUT)				# Output to control the MP10 PUMP 
GPIO.setup(12, GPIO.OUT)				# Output to control the DISPLAY PUMP

#GPIO.setup(X, GPIO.OUT)				# Output to control the SKIMMER
#GPIO.setup(X, GPIO.OUT)				# Output to control the AUTO TOP OFF in the event of a power interupt

# pin set up for the pair of float sensors in the skimmer overflow chamber
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)		


# Set 1 input for the 'Open Door' push button
# Set 1 inputs from the RODI tank for monitoring 10% of RODI levels
# Set 1 input as to whether the auto feeding is set to on
# Future expansion - humidity of sump? Salinity level?

# Set output pin to turn on the ZeoVit tank mixer pump
# Set 3 outputs for the tri-color LED
# Set output pin for the buzzer


###################################################################
# Set up variables and constants used in control

# Seneye connection constants
seneye_url = 'https://api.seneye.com/v1/devices/45041/exps?user=nickbarsley@cantab.net&pwd=Qpwals0'

# Loop control
timer_feeding = 0
duration_feeding = 10*60						# Duration in loop cycles
state_feeding = False
state_leak = False
state_has_changed = False
	
# Constants - ideas:
# Frequency of required sample rate for different sensor inputs
sample_freq_seneye = 15*60											# 15 mins

	
	# Frequency of storing to the cloud for different sensor inputs
	# Definition of acceptable ranges and states
	# Log in details for cloud providers
	# Log in details for email and phone numbers
	
	
###################################################################
# Main loop


while True:

	# know what time it is
	time_now = datetime.now()
	time_now_string = "{:d}:{:02d}".format(time_now.hour, time_now.minute)
	screen_message = time_now_string
	
	# wdt.kep_alive()

	# Read and store (cloud) values of all sensors - to do - varying frequency of sampling / recording based on sensor type
	sensor_leak_1 = GPIO.input(25)
	sensor_leak_2 = GPIO.input(24)
	sensor_leak_3 = GPIO.input(23)
	sensor_feeding = GPIO.input(26)
	sensor_skimmate_tank_full = GPIO.input(21)
	
	# Analyse signals for disrepancy (again varying frequency of doing this)
	if state_leak == False:
		if sensor_leak_1==0 or sensor_leak_2==0 or sensor_leak_3==0:				# Any of the sensors are detecting a leak
			state_leak = True
	
	# Feeding variable control
	if sensor_feeding==0: 			# Push button has been pressed
		state_feeding =	True
		timer_feeding = 0
		state_has_changed = True
		state_leak = False
		
	if sensor_skimmate_tank_full==0:
		state_skimmate_tank_full = True
		screen_message = "Skimmer full!"
		
	
	if state_feeding == True:		# Feeding mode is on
		if timer_feeding < duration_feeding:					
			timer_feeding += 1
			screen_message = "Pumps off\nOn in " + str(int(((duration_feeding - timer_feeding) / 60))) + " mins"
		else:
			state_feeding = False
			state_has_changed = True
			timer_feeding = 0

			
	# Implement controller rules as required


	if state_has_changed == True:
		if state_feeding == True:
			GPIO.output(05,True)		# Return pump OFF
			time.sleep(0.3)
			GPIO.output(06,True)		# MP10 OFF
			time.sleep(0.3)
			GPIO.output(12,True)		# Display pump 2 OFF
			time.sleep(0.3)
	
		if state_feeding == False:
			GPIO.output(05,False)		# Return pump ON
			time.sleep(0.3)
			GPIO.output(06,False)		# MP10 ON
			time.sleep(300)			
			GPIO.output(12,False)		# Display pump 2 ON
			time.sleep(0.3)
		state_has_changed = False
		
	if state_leak == True:				# Outside state change as other states might turn back on pumps
		GPIO.output(05,True)		# Return pump OFF
		# GPIO.output(05,True)		# Skimmer OFF
		# Turn off return pump and skimmer
		# EMail me & MC
		# Text me & MC
		# Call me & MC
		screen_message = "EEEK!! A LEAK!!!"			

	if (time_now.hour >= 21) or (time_now.hour < 7):
		lcd.set_backlight(0)
	else:
		# Reporting
		lcd.clear()
		lcd.set_backlight(1)
		lcd.message(screen_message)
	
	time.sleep(0.3)
	
	
	# Ideas on rules:
		# If Friday - send update email
		# Check whether any leaks?
			# If so, alarm to me and shut off return pump
		# Check whether a button press for:
			# Feeding
			# Door open
		# Check if temperatures are ok
			# If out of limits send an alarm
			# Perhaps use secondary heater to take temp control even finer?
		# Check levels in:
			# RODI
				# Alarm if too low
			# Skimmer overflow tank
				# Shut off skimmer and alarm if high
			# Sump
				# Shut off return pump and alarm if high
			# Display
				# Shut off return pump and alarm if high
			
	# Check maintenance schedule daily
		# Prompt if maintenance needed
		# Water Change
		# Test sensors
		# Test water parameters
		# Cleaning of sump, display tank, etc...
		# Return pump maintenance
		# Replace heater
		
	# Send period email status updates

	# End of loop activities
