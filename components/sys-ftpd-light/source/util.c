#include <string.h>
#include <stdio.h>
#include <malloc.h>
#include <math.h>
#include <unistd.h>

#include <switch.h>

bool paused = false;
static Mutex pausedMutex;
void pauseInit() {
    mutexInit(&pausedMutex);
    mutexLock(&pausedMutex);
    FILE *should_pause_file = fopen("/config/sys-ftpd/ftpd_paused", "r");
    if (should_pause_file != NULL) {
        paused = true;
        fclose(should_pause_file);
    }
    mutexUnlock(&pausedMutex);
}


bool isPaused() {
    mutexLock(&pausedMutex);
    bool ret = paused;
    mutexUnlock(&pausedMutex);
    return ret;
}

void setPaused(bool newPaused) {
    mutexLock(&pausedMutex);
    paused = newPaused;
    if(paused) {
        FILE *should_pause_file = fopen("/config/sys-ftpd/ftpd_paused", "w");
        fclose(should_pause_file);
    } else {
        unlink("/config/sys-ftpd/ftpd_paused");
    }
    mutexUnlock(&pausedMutex);
}
