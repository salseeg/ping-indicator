SHELL=/bin/bash

CURRENT_VERSION := $(shell cat pkg/DEBIAN/control | grep Version: | cut -f 2 -d ' ')

.PHONY: pkg

pkg:
	dpkg-deb -b pkg ping-indicator_$(CURRENT_VERSION).deb
