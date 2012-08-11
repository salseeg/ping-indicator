#!/usr/bin/env python
# coding: utf-8



import gtk
import appindicator
import data_exch
import time
import Image
import os.path

LOGO = os.path.expanduser("~/.ping-indicator/imgs/over.png")
UPDATE_TIMEOUT = 1000  # ms

MAX_PING = 100 # ms

IMAGES_DIR = os.path.expanduser("~/.ping-indicator/imgs/")
IMAGES_EXT = '.png'
IMAGES_THEME = 'dark'
IMAGES_INDICATOR_FORMAT = "{}ping-indicator-status-{}.png"
TMP_DIR = os.path.expanduser("~/.ping-indicator/tmp/")

MENU_HOST_FORMAT =  "{}  : {} ms"
MENU_HOST_SEPARATOR = "  : "

def delay_to_filename(delay):
	fn_prefix = IMAGES_DIR
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
	return fn

class IconCache :
	def __init__(self):
		self.images = dict()
		for i in range(0,10):
			img = Image.open(self._build_filename(i))
			self.images[i] = img
		self.images['none'] = Image.open(self._build_filename('none'))
		self.images['over'] = Image.open(self._build_filename('over'))
		
	def _build_filename(self, name):
		fn = IMAGES_DIR
		if (name == 'over') or (name == 'none') :
			fn += name + IMAGES_EXT
		else:
		 	fn += 'dark_' + str(name) + IMAGES_EXT 
		return fn
	
	def image_by_delay(self, delay):
		if delay > 0 :
			ind = int(delay / (MAX_PING / 10))
			if ind > 10 :
				ind = 'over'
		else:
			ind = 'none'
		return self.images[ind]
	



class AppIndicator (object):

    	def __init__(self):
		self.icons = IconCache();
        	self.ind = appindicator.Indicator("ping-indicator-applet",
        	    LOGO, appindicator.CATEGORY_APPLICATION_STATUS)
        	self.ind.set_status (appindicator.STATUS_ACTIVE)
		self.menu = gtk.Menu()
		sep = gtk.SeparatorMenuItem()
		item = gtk.MenuItem()
		item.add(gtk.Label("exit"))

		self.menu.append(sep)
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
				icon = self.icons.image_by_delay(delay)
				img.paste(icon, (i * 8, 0))
				i += 1

			suffix = int(time.time()) % 4
			indicator_fn = IMAGES_INDICATOR_FORMAT.format(TMP_DIR, suffix)
			img.save(indicator_fn)
			self.ind.set_icon( indicator_fn )
			self.update_menu(data)
		return True

	def build_menu(self,data):
		i = 0;
		for host, delay in data:
			item = gtk.MenuItem()
			item.add(gtk.Label(MENU_HOST_FORMAT.format(host, round(delay,1))))
			self.menu.insert(item, i)
			i += 1



	def update_menu(self, data):

		items = self.menu.get_children()
		first_one = items[0]
		first_host, first_delay = data[0]
		if (first_one.get_label().split(MENU_HOST_SEPARATOR)[0] != first_host) :
			self.build_menu(data)
			self.menu.show_all()
		else:
			i = 0
			for host, delay in data:
				item = items[i]
				item.set_label(MENU_HOST_FORMAT.format(host, round(delay,1)))
				i += 1

		self.ind.set_menu(self.menu)
		
	
   


indicator = AppIndicator()
gtk.main()

