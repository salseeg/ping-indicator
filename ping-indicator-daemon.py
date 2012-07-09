#!/usr/bin/env python


from ping import Ping, is_valid_ip4_address 
import time
import math
import socket
import conf
import data_exch
import signal



import sys

PING_FREQUENCY = 1 # HZ


def signal_handler(a,b):
	sys.exit(0)


def make_ping_object(h):
	timeout = 500;
	if not is_valid_ip4_address(h):
		h = socket.gethostbyname(h)
	return Ping(h, timeout)


class PingIndicatorDaemon:
	def __init__(self, hostnames):
		self.init_pinger(hostnames)


	def main(self):
		while True :
			to_sleep = 1000 / PING_FREQUENCY;
        		used = self.pinger()
			to_sleep -= used
			to_sleep = max(to_sleep, 0)
			time.sleep(to_sleep/1000)

	def quit(self):
		sys.exit(0)

	def init_pinger(self, hostnames):
		self.hostnames = hostnames
		self.hosts = [ make_ping_object(h) for h in hostnames ]


	def pinger(self):
		delays = []
		sum = 0;

		i = 0
		for h in self.hosts :
			delay = h.do()
			if delay is None :
				delay = -1
				sum += 500
			else:
				sum += delay;
			delays.append( (self.hostnames[i], delay) )
			i += 1
			
	 	self.show_results(delays)
		
		return sum

	def show_results(self, delays) :
		data = data_exch.Data_Exch()
		data.write(delays)


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGHUP, signal_handler)
	c = conf.Conf()
	
	deamon = PingIndicatorDaemon(c.servers)
     	deamon.main()




















