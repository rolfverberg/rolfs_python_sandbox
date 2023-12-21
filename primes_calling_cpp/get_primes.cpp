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
