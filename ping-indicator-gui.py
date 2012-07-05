#!/usr/bin/env python
# coding: utf-8


LOGO = "/home/salseeg/projects/ping-appindicator/imgs/over.png"
UPDATE_TIMEOUT = 1000  # ms

import gtk
import appindicator
import data_exch
import time


class AppIndicator (object):

    	def __init__(self):
        	self.ind = appindicator.Indicator("ping-indicator_applet",
        	    LOGO, appindicator.CATEGORY_APPLICATION_STATUS)
        	self.ind.set_status (appindicator.STATUS_ACTIVE)
		self.menu = gtk.Menu()
		item = gtk.MenuItem()

		item.add(gtk.Label("hello world"))
		# item.add(gtk.Entry())

		self.menu.append(item)
		self.menu.show_all()
		self.ind.set_menu(self.menu)
		gtk.timeout_add(UPDATE_TIMEOUT, self.update)

	def update(self):
		data_file = data_exch.Data_Exch()
		data = data_file.read()
		if data :
			for host, delay in data:
				fn_prefix = "home/salseeg/projects/ping-appindicator/imgs/"
				ind = int(round(delay / 50))
				fn = 'dark_{}'.format(ind)
				if ind > 10 : 
					fn = 'over'
				if ind < 0 :
					fn = 'none'
				
				fn = fn_prefix + fn + '.png'
				print fn+"\n"

				self.ind.set_icon( fn )
				time.sleep(0.2)
   


indicator = AppIndicator()
gtk.main()

