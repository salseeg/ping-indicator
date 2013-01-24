#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define RELPATH "/usr/share/ping-indicator/python/ping-indicator-daemon.py"


int main(int argc, char ** argv){
	char ** empty;
	
	execv(RELPATH, empty);
	return 0;
}
