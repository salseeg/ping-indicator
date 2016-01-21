.PHONY : all

all:
    dpkg -b pkg ping-indicator_`cat pkg/DEBIAN/control| grep Version: | cut -f 2 -d ' '`.deb