#!/usr/bin/env python
# coding: utf-8


import os
import time


class Data_Exch :
	def __init__(self):
		self.filename = os.path.expanduser("~/.ping-indicator/tmp/ping-indicator.data")
		#self.read()
	def read(self):
		if os.path.exists(self.filename):
			t = int(time.time())
			delays = []
			if t - int(os.path.getmtime(self.filename))  < 3 :
				f = open(self.filename, "r")
				for line in f :
					parts = line.strip().split(':')
					delays.append( (parts[0], float(parts[1])) )
				f.close()
			else: # indicating deamon died
				ind = t % 4
				delays.append( ("no", 0.1))
				delays.append( ("fresh", 0.1))
				delays.append( ("data", 0.1))
				delays.append( ("found", 0.1))
				host, data = delays[ind]
				delays[ind] = (host, 10000)

			return delays
		return false
	def write(self, delays):

		f = open(self.filename, "w")
		for host, delay in delays:
			f.write("{}:{}\n".format(host,delay))
		f.close()



