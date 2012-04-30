#!/usr/bin/env python


from ping import Ping, is_valid_ip4_address 
import time
import math
import socket



import sys
import gtk
import appindicator

PING_FREQUENCY = 1 # seconds

class PingIndicator:
	def __init__(self):
        	self.ind = appindicator.Indicator("salseeg's-ping-indicator",
                                            "indicator-messages",
                                            appindicator.CATEGORY_APPLICATION_STATUS)
         	self.ind.set_status(appindicator.STATUS_ACTIVE)
         	self.ind.set_attention_icon("new-messages-red")

         	self.menu_setup()
         	self.ind.set_menu(self.menu)
	def menu_setup(self):
        	self.menu = gtk.Menu()
		
		self.quit_item = gtk.MenuItem("Quit")
         	self.quit_item.connect("activate", self.quit)
         	self.quit_item.show()
         	self.menu.append(self.quit_item)

	def main(self):
        	self.pinger()
         	gtk.timeout_add(PING_FREQUENCY * 1000, self.pinger)
         	gtk.main()

	def quit(self, widget):
		sys.exit(0)

    	def check_mail(self):
		# messages, unread = self.gmail_checker('myaddress@gmail.com','mypassword')
		#if unread > 0:
		# 	self.ind.set_status(appindicator.STATUS_ATTENTION)
		#else:
		#	self.ind.set_status(appindicator.STATUS_ACTIVE)
         	return True

	def pinger(self):
		pass
		return True


if __name__ == "__main__":
     indicator = CheckGMail()
     indicator.main()















def make_ping_object(h):
	timeout = 500;
	if not is_valid_ip4_address(h):
		h = socket.gethostbyname(h)
	return Ping(h, timeout)


def show_results(delays):
	for tup in delays : 
		(host, delay) = tup
		print host, delay
	print


if __name__ == '__main__' :
	hostnames = [
		'89.185.10.2'
		, '89.185.8.30'
		, '89.185.8.31'
		, '89.185.8.51'
		, '89.185.8.52'
		, '89.185.8.53'
		, '89.185.8.54'
		, '89.185.8.65'
		, '8.8.8.8'
		, 'i.ua'
	]


	hosts = [ make_ping_object(h) for h in hostnames ]

	while 1 :
		iteration_start_time = time.time()
		delays = []

		i = 0
		for h in hosts :
			delay = h.do()
			delays.append( (hostnames[i], delay) )

#			if delay > 0 :
#				s += chr(int(math.floor(48 + delay/10)))
#			else:
#				s +='-'
			i += 1
			
	 	show_results(delays)
		
		iteration_end_time = time.time()
		to_sleep = 0.99 - iteration_end_time + iteration_start_time
		if (to_sleep > 0) :
			time.sleep(to_sleep)
