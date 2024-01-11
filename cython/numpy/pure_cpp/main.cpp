#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

#define MIN(a,b) (((a)<(b))?(a):(b))
#define MAX(a,b) (((a)>(b))?(a):(b))

int clip(const int a, const int min_value, const int max_value) {
  if (a <= min_value) {
    return min_value;
  } else if (a >= max_value) {
    return max_value;
  } else {
    return a;
  }
}

void compute(
    const int* const array_1, const int* const array_2, int* const result,
    size_t array_size, int a, int b, int c) {
  size_t i;
  const int *array_1ptr = array_1;
  const int *array_2ptr = array_2;
  int *resultptr = result;
  for (i = 0; i < array_size; i++, array_1ptr++)
//    (*resultptr++) = clip(*array_1ptr, 2, 10) * a + (*array_2ptr++) * b + c;
    (*resultptr++) = MIN(MAX(*array_1ptr, 2), 10) * a + (*array_2ptr++) * b + c;
}

int get_sum(const int* const a, const size_t num) {
  size_t i;
  int sum = 0.0;
  const int *aptr = a;
  for (i = 0; i < num; i++)
    sum += (*aptr++);
  return sum;
}

double get_mean(const double* const a, const size_t num) {
  size_t i;
  double sum = 0.0;
  const double *aptr = a;
  for (i = 0; i < num; i++)
    sum += (*aptr++);
  return sum/num;
}

double get_stdv(const double* const a, const size_t num) {
  double mean = get_mean(a, num);
  size_t i;
  double dummy, sum = 0.0;
  const double *aptr = a;
  for (i = 0; i < num; i++) {
    dummy = (*aptr++) - mean;
    sum += dummy * dummy;
  }
  return sqrt(sum/num);
}

int main() {

  const size_t num_row = 3000;
  const size_t num_column = 2000;
  const int a = 4;
  const int b = 3;
  const int c = 9;
  const int n = 100;

  double *run_times = new double[n];

  size_t i;
  int **array_1, **array_2, **result;
  array_1 = new int*[num_row];
  array_1[0] = new int[num_row * num_column];
  array_2 = new int*[num_row];
  array_2[0] = new int[num_row * num_column];
  result = new int*[num_row];
  result[0] = new int[num_row * num_column];
  for (i = 1; i < num_row; i++) {
    array_1[i] = array_1[i-1] + num_column;
    array_2[i] = array_2[i-1] + num_column;
    result[i] = result[i-1] + num_column;
  }

  int *array_1ptr = array_1[0];
  int *array_2ptr = array_2[0];
  int *resultptr = result[0];
  for (i = 1; i < num_row*num_column; i++) {
    (*array_1ptr++)  = rand() % 1000;
    (*array_2ptr++)  = rand() % 1000;
    (*resultptr++)  = rand() % 1000;
  }

  struct timeval t0, t1;
  double *run_timesptr = run_times;
  for (i = 0; i < n; i++) {
    gettimeofday(&t0, NULL);
    compute(array_1[0], array_2[0], result[0], num_row*num_column, a, b, c);
    gettimeofday(&t1, NULL);
    (*run_timesptr++) = 1000.0 * (t1.tv_sec - t0.tv_sec) + (t1.tv_usec - t0.tv_usec) / 1.e3;
  }
  fprintf(stdout, "\nRunning compute took %f +- %f ms\n\n",
    get_mean(run_times, n), get_stdv(run_times, n));

  fprintf(stdout, "sum = %d\n\n", get_sum(result[0], num_row*num_column));

  gettimeofday(&t0, NULL);
  for (i = 0; i < n; i++) {
    compute(array_1[0], array_2[0], result[0], num_row*num_column, a, b, c);
  }
  gettimeofday(&t1, NULL);
  double run_time = 1000.0 * (t1.tv_sec - t0.tv_sec) + (t1.tv_usec - t0.tv_usec) / 1.e3;
  fprintf(stdout, "\nRunning as one took an average of %f ms per compute\n\n", run_time/n);
  delete[] run_times;
  delete[] array_1[0];
  delete[] array_1;
  delete[] array_2[0];
  delete[] array_2;
  delete[] result[0];
  delete[] result;
}
