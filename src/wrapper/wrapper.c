#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#define REAL_PATH "/usr/share/ping-indicator/python/ping-indicator-daemon.py"


int main(int argc, char ** argv){
	char * user = NULL ;
	user = malloc(100);
	printf("argc = %d\n", argc);

	if (argc > 1){
		strncpy(user, argv[1], 80);
		char *const parmList[] = {REAL_PATH, user, NULL};
	
		//printf("%s\n", user);
		execv(REAL_PATH,  parmList);
		return 0;
	}else{
		return -1;
	}
}
