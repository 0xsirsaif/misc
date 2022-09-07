#include <stdio.h>
#include <time.h>
#include <stdlib.h>

#define WEEK_LEN 7

int nweek(void){
    // get current time
    time_t now = time(NULL);
    if (now == -1){
        return EXIT_FAILURE;
    }
    // get tm struct for localtime
    struct tm *local = localtime(&now);
    if (local == NULL){
        return EXIT_SUCCESS;
    }
    int nday = local->tm_yday;
    /*
     Algorithm:
     -
     * */
    if ((nday % WEEK_LEN) != 0){
        return (nday / WEEK_LEN) + 1;
    }
    return nday / WEEK_LEN;
}

int main(void){
    printf("%d\n", nweek());
    return EXIT_SUCCESS;
}