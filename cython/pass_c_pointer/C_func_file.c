#include "C_func_file.h"

#include <stdlib.h>

void multiply_by_10_in_C(double* const arr, unsigned int n)
{
    unsigned int i;
    double *arrptr= arr;
    for (i = 0; i < n; i++) {
        fprintf(stdout,"%d: %p\n", i, arrptr);
        (*arrptr++) *= 10;
    }
}
