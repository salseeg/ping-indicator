#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define RELPATH "/.ping-indicator/bin/ping-indicator-daemon.py"

char path[200];

int main(int argc, char ** argv){
	char *s;
	s = getenv("HOME");
	strncpy(path, s, 199);
	strncat(path, RELPATH, 199);
	printf("%s\n", path);
	execv(path, argv);
	return 0;
}
