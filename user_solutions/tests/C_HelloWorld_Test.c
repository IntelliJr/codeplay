#include <stdio.h>
#include <assert.h>
#include "C_HelloWorld.c"

// Function to test
char *helloWorld();

int main() {
    assert(helloWorld() == "Hello World");
    printf("All tests passed successfully! Ready to submit solution.\n");

    return 0;
}