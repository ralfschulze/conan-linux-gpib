#include <stdlib.h>
#include <stdio.h>
#include "gpib/ib.h"

int main() {

    char *version;
    ibvers(&version);
    printf("linux gpib v%s\n", version);
}
