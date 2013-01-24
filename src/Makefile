.PHONY : all suid

all: ping-indicator-daemon-wrapper

ping-indicator-daemon-wrapper: wrapper.c
	gcc -o ping-indicator-daemon-wrapper wrapper.c
	chmod a+x ping-indicator-daemon-wrapper

suid: ping-indicator-daemon-wrapper
	chown root ping-indicator-daemon-wrapper
	chmod +s ping-indicator-daemon-wrapper
