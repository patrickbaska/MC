#!/usr/bin/env python
     
import os
import re
import time
import math
     
def main():
     
# checks the last reading entered in txt file or numeric field from DB
	def curreading():
		while(1):
			reading = open("readings.html", "r")
			curreading = reading.readline(4)
			reading.close()
			return float(curreading)
     
# set desired alarm threshold using threshold file from web server. reads a text file in /var/bin or numeric field from DB.               
	def alarmthresh():
		readthresh = open("threshold.html", "r")
		alarmthresh = readthresh.readline(4)
		readthresh.close()
		return float(alarmthresh)
	
# monitor the readings in the cur_reading.
	def monreading():
		if curreading() >= alarmthresh():
			time.sleep(5)
			print "Zone Status: Zone Clear", curreading()
			time.sleep(5)
		else:
			if curreading() <= alarmthresh():
				time.sleep(5)
				print "Zone Status: Alert Zone Alarm", curreading()
				time.sleep(5)

# this constructs an infinite loop
	infloop = 1
	while infloop == 1:
		monreading()
     
if __name__ == '__main__':
		main()
