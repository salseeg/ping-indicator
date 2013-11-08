#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define RELPATH "/usr/share/ping-indicator/python/ping-indicator-daemon.py"


int main(int argc, char ** argv){
	char user[80] = "\0" ;

	if (argc > 1){
		strncpy(user, argv[1], sizeof(user) -1);
	
		execv(RELPATH, (char* const* ) user);
		//printf("%s\n", user);
		return 0;
	}else{

		return -1;
	}
}
