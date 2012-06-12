#!/usr/bin/env python
# coding: utf-8


import gtk
import appindicator

class AppIndicator (object):

    def __init__(self):
        self.ind = appindicator.Indicator("hello world client",
            "distributor-logo", appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status (appindicator.STATUS_ACTIVE)
        self.menu = gtk.Menu()
        item = gtk.MenuItem()

        item.add(gtk.Label("hello world"))
        # item.add(gtk.Entry())

        self.menu.append(item)
        self.menu.show_all()
        self.ind.set_menu(self.menu)


indicator = AppIndicator()
gtk.main()

