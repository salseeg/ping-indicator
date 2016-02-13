.PHONY: all pkg clean check_deb

SHELL=/bin/bash
CURRENT_VERSION := $(shell cat pkg/DEBIAN/control | grep Version: | cut -f 2 -d ' ')

all: check_deb

pkg: clean
	
	mkdir -p pkg/usr/bin pkg/usr/share/ping-indicator 
	$(MAKE) -C src/wrapper/ into_pkg
	cp -r src/indicator/* pkg/usr/share/ping-indicator/
	cp -r imgs pkg/usr/share/ping-indicator/
	chmod 755 pkg/usr pkg/usr/bin pkg/usr/share 
	dpkg-deb -b pkg ping-indicator_$(CURRENT_VERSION).deb

clean:
	rm -rf pkg/usr

check_deb: pkg
	lintian ping-indicator_$(CURRENT_VERSION).deb
