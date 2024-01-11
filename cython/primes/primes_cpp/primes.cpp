#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>

int get_primes(const int num_primes, int *primes)
{
  if (!primes) return -1;

  int i = 2, j, num = 0;
  int *primesptr = NULL;
  int *lastprime = primes;
  while (num < num_primes) {
    primesptr = primes;
    for (j = 0; j < num && i % (*primesptr); j++, primesptr++);
    if (j == num) {
      (*lastprime++) = i;
      ++num;
    }
    ++i;
  }
  return num;
}

int get_num_primes(const int num, int *primes)
{
  if (!primes) return -1;

  int i, j, n = 0;
  int *primesptr = NULL;
  int *lastprime = primes;
  for (i = 2; i < num; i++) {
    primesptr = primes;
    for (j = 0; j < n && i % (*primesptr); j++, primesptr++);
    if (j == n) {
      (*lastprime++) = i;
      ++n;
    }
  }
  return n;
}


int main() {
  int num_primes = 100;
  int *primes = new int[num_primes];
  if (!primes) fprintf(stderr, "Memory allocation failed");
  struct timeval t0, t1;
  gettimeofday(&t0, NULL);
  int num = get_primes(num_primes, primes);
  gettimeofday(&t1, NULL);
  printf("\nThe first %d prime numbers are:\n", num);
  for (int i = 0, *primesptr=primes; i < num; i++) {
    printf(" %d", (*primesptr++));
  }
  double run_time = (t1.tv_sec - t0.tv_sec) + (t1.tv_usec - t0.tv_usec) / 1.e6;
  printf("\nRunning get_primes(%d) took %f seconds\n\n",
    num_primes, run_time);
  delete[] primes;

  num = 10000;
  primes = new int[num];
  if (!primes) fprintf(stderr, "Memory allocation failed");
  gettimeofday(&t0, NULL);
  num_primes = get_num_primes(num, primes);
  gettimeofday(&t1, NULL);
  printf("\nThe number of primes in [0:%d] is %d\n", num, num_primes);
  run_time = (t1.tv_sec - t0.tv_sec) + (t1.tv_usec - t0.tv_usec) / 1.e6;
  printf("\nRunning get_num_primes(%d) took %f seconds\n\n",
    num, run_time);
  delete[] primes;

  return 0;
}
