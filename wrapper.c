#include <unistd.h>

#define REAL_PATH "/home/salseeg/projects/ping-appindicator/ping-indicator-daemon.py"

int main(int argc, char ** argv){
	execv(REAL_PATH, argv);
	return 0;
}
