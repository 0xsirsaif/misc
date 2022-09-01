#include <stdio.h>
#include <string.h>

void print_array(void *array);
void itoa(int number, char string[]);
int power(char base, int exp);
void reverse_string(char string[]);

int power(char base, int exp){
    int result = 1;
    for (int i = 0; i < exp; ++i) {
        result *= base - '0';
    }
    return result;
}
void reverse(char string[]){
    int i, j, c;
    for (i = 0, j = strlen(string)-1; i < j; i++, j--) {
        c = string[i];
        string[i] = string[j];
        string[j] = c;
    }
}
