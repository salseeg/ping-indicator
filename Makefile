.PHONY: all pkg clean check_deb prepare_pkg prepare_pkg_dir bin_64 bin_32 do_prepare_pkg

SHELL=/bin/bash
CURRENT_VERSION := $(shell cat pkg/DEBIAN/control | grep Version: | cut -f 2 -d ' ')
CURRENT_DATE := $(shell date -R )

all: check_deb

prepare_pkg_dir: 
	mkdir -p pkg/usr/bin pkg/usr/share/ping-indicator pkg/usr/share/doc/ping-indicator pkg/usr/share/man/man1
bin_32:
	$(MAKE) -C src/wrapper/ into_pkg_32

bin_64: 
	$(MAKE) -C src/wrapper/ into_pkg


prepare_pkg: clean prepare_pkg_dir bin_64 do_prepare_pkg

do_prepare_pkg:
	cp debian/changelog pkg/usr/share/doc/ping-indicator/changelog.Debian	 
	gzip -n --best pkg/usr/share/doc/ping-indicator/changelog.Debian		
	cp debian/copyright pkg/usr/share/doc/ping-indicator/copyright		
	cp debian/ping-indicator-deamon-wrapper.1.man pkg/usr/share/man/man1/ping-indicator-daemon-wrapper.1		
	gzip -n --best pkg/usr/share/man/man1/ping-indicator-daemon-wrapper.1
	cp -r src/indicator/* pkg/usr/share/ping-indicator/
	rm -r pkg/usr/share/ping-indicator/python/tests/
	cp -r imgs pkg/usr/share/ping-indicator/
	chmod 755 pkg/usr pkg/usr/bin pkg/usr/share pkg/usr/share/ping-indicator \
			pkg/usr/share/ping-indicator/python \
			pkg/usr/share/ping-indicator/imgs \
			pkg/usr/share/ping-indicator/ui \
			pkg/usr/share/doc/ping-indicator/ \
			pkg/usr/share/doc/ \
			pkg/usr/share/man \
			pkg/usr/share/man/man1 \
			pkg/usr/bin/ping-indicator-daemon-wrapper \
			pkg/usr/share/ping-indicator/python/ping-indicator-gui.py \
			pkg/usr/share/ping-indicator/python/ping-indicator-daemon.py \
			pkg/DEBIAN/post* \
			pkg/usr/share/ping-indicator/ui
	chmod 644 pkg/usr/share/ping-indicator/imgs/* \
			pkg/usr/share/ping-indicator/python/ping.py \
			pkg/usr/share/ping-indicator/python/data_exch.py \
			pkg/usr/share/ping-indicator/python/conf.py \
			pkg/usr/share/doc/ping-indicator/copyright \
			pkg/usr/share/doc/ping-indicator/changelog.Debian.gz \
			pkg/usr/share/man/man1/ping-indicator-daemon-wrapper.1.gz \
			pkg/usr/share/ping-indicator/ui/conf.glade
	strip pkg/usr/bin/ping-indicator-daemon-wrapper
	fakeroot chown -R root:root pkg/usr pkg/DEBIAN/post*

pkg: prepare_pkg
	fakeroot dpkg-deb -b pkg ping-indicator_$(CURRENT_VERSION)_amd64.deb

pkg32: clean prepare_pkg_dir bin_32 do_prepare_pkg
	sed -i 's/Architecture: amd64/Architecture: i386/' pkg/DEBIAN/control
	fakeroot dpkg-deb -b pkg ping-indicator_$(CURRENT_VERSION)_i386.deb
	sed -i 's/Architecture: i386/Architecture: amd64/' pkg/DEBIAN/control

clean:
	fakeroot rm -rf pkg/usr
	rm -f src/indicator/python/*.pyc
	rm -f src/indicator/python/*/*.pyc

check_deb: pkg
	lintian ping-indicator_$(CURRENT_VERSION)_amd64.deb
