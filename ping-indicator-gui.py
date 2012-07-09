#!/usr/bin/env python
# coding: utf-8


LOGO = "/home/salseeg/projects/ping-appindicator/imgs/over.png"
UPDATE_TIMEOUT = 1000  # ms

import gtk
import appindicator
import data_exch
import time
import Image
import os.path


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
			count = len(data)
			img = Image.new("RGBA",(count*8,20))
			i = 0;
			for host, delay in data:
				fn_prefix = "/home/salseeg/projects/ping-appindicator/imgs/"
				if delay > 0 :
					ind = int(delay / 50.0)
				else:
					ind = -1;
				fn = 'dark_{}'.format(ind)
				if ind > 10 : 
					fn = 'over'
				if ind < 0 :
					fn = 'none'
				fn = fn_prefix + fn + '.png'
				icon = Image.open(fn);
				img.paste(icon, (i * 8, 0))
				
				i += 1
			suffix = int(time.time()) % 4
			indicator_fn = "/tmp/ping-indicator-status-{}.png".format(suffix)
			img.save(indicator_fn)
			self.ind.set_icon( indicator_fn )
		return True
		
	
   


indicator = AppIndicator()
gtk.main()

