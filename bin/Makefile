.PHONY : all suid

all: ping-indicator-deamon-wrapper

ping-indicator-deamon-wrapper: wrapper.c
	gcc -o ping-indicator-deamon-wrapper wrapper.c
	chmod a+x ping-indicator-deamon-wrapper

suid: ping-indicator-deamon-wrapper
	chown root ping-indicator-deamon-wrapper
	chmod +s ping-indicator-deamon-wrapper
