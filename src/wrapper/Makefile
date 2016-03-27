.PHONY : all suid into_pkg into_pkg_32 

all: ping-indicator-daemon-wrapper 

ping-indicator-daemon-wrapper-32: wrapper.c
	export CFLAGS=-m32
	gcc -m32 -o ping-indicator-daemon-wrapper wrapper.c
	chmod a+x ping-indicator-daemon-wrapper

ping-indicator-daemon-wrapper: wrapper.c
	gcc -o ping-indicator-daemon-wrapper wrapper.c
	chmod a+x ping-indicator-daemon-wrapper

suid: ping-indicator-daemon-wrapper
	chown root ping-indicator-daemon-wrapper
	chmod +s ping-indicator-daemon-wrapper

into_pkg: all
	mv ping-indicator-daemon-wrapper ../../pkg/usr/bin/

into_pkg_32: ping-indicator-daemon-wrapper-32 
	mv ping-indicator-daemon-wrapper ../../pkg/usr/bin/

