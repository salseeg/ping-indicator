#!/usr/bin/env python
# coding: utf-8


import os


class Data_Exch :
	def __init__(self):
		self.filename = "/tmp/ping-indicator.data"
		#self.read()
	def read(self):
		if os.path.exists(self.filename):
			delays = []
			f = open(self.filename, "r")
			for line in f :
				parts = line.strip().split(':')
				delays.append( (parts[0], float(parts[1])) )
			f.close()
			return delays
		return false
	def write(self, delays):

		f = open(self.filename, "w")
		for host, delay in delays:
			f.write("{}:{}\n".format(host,delay))
		f.close()



