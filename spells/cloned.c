#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ftw.h>

static char *ROOT_DIRECTORY = "/media/data/open-source";

bool is_cloned(char repo_url){

    return false;
}

int list(const char *name, const struct stat *status, int type) {
    // call failed on fpath
    if(type == FTW_NS)
        return 0;

    // if fpath is a regular file
//    if(type == FTW_F)
//        printf("0%3o\t%s\n", status->st_mode&0777, name);

    // fpath is a directory
    //  && strcmp(".", name) != 0 ?
    if(type == FTW_D)
        printf("%s/\n", name);

    return 0;
}

int main(int argc, char *argv[]){
    ftw(ROOT_DIRECTORY, list, 1);
    return 0;
}
