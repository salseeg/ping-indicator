.PHONY: all pkg clean check_deb prepare_pkg

SHELL=/bin/bash
CURRENT_VERSION := $(shell cat pkg/DEBIAN/control | grep Version: | cut -f 2 -d ' ')

all: check_deb

prepare_pkg: clean
	mkdir -p pkg/usr/bin pkg/usr/share/ping-indicator pkg/usr/share/doc/ping-indicator
	git log --pretty=oneline | gzip --best > pkg/usr/share/doc/ping-indicator/changelog.Debian.gz		 
	$(MAKE) -C src/wrapper/ into_pkg
	cp -r src/indicator/* pkg/usr/share/ping-indicator/
	cp -r imgs pkg/usr/share/ping-indicator/
	chmod 755 pkg/usr pkg/usr/bin pkg/usr/share pkg/usr/share/ping-indicator \
			pkg/usr/share/ping-indicator/python \
			pkg/usr/share/ping-indicator/imgs \
			pkg/usr/share/ping-indicator/ui \
			pkg/usr/bin/ping-indicator-daemon-wrapper \
			pkg/usr/share/ping-indicator/python/ping-indicator-gui.py \
			pkg/usr/share/ping-indicator/python/ping-indicator-daemon.py \
			pkg/usr/share/ping-indicator/ui
	chmod 644 pkg/usr/share/ping-indicator/imgs/* \
			pkg/usr/share/ping-indicator/python/ping.py \
			pkg/usr/share/ping-indicator/python/data_exch.py \
			pkg/usr/share/ping-indicator/python/conf.py \
			pkg/usr/share/ping-indicator/ui/conf.glade
	strip pkg/usr/bin/ping-indicator-daemon-wrapper
	sudo chown -R root:root pkg/usr 

pkg: prepare_pkg
	dpkg-deb -b pkg ping-indicator_$(CURRENT_VERSION).deb

clean:
	sudo rm -rf pkg/usr

check_deb: pkg
	lintian ping-indicator_$(CURRENT_VERSION).deb
