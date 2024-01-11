#include "compute_c.h"

int clip(const int a, const int min_value, const int max_value) {
  if (a <= min_value) {
    return min_value;
  } else if (a >= max_value) {
    return max_value;
  } else {
    return a;
  }
}

void compute_in_c(const int* const array_1, const int* const array_2, int* const result,
    size_t array_size, int a, int b, int c) {
  size_t i;
  const int *array_1ptr = array_1;
  const int *array_2ptr = array_2;
  int *resultptr = result;
  for (i = 0; i < array_size; i++)
    (*resultptr++) = clip(*array_1ptr++, 2, 10) * a + (*array_2ptr++) * b + c;
}
