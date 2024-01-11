#ifndef PRIMES_H
#define PRIMES_H

#include <stdlib.h>

class Primes {

  private:

    size_t num_primes;
    size_t *primes;

  public:

/*    Primes(void) : num_primes(0), primes(NULL)
    {
      fprintf(stdout, "\nAllocating an empty Primes object (num_primes = %zu)\n", num_primes);
    }*/
    Primes(const size_t num) : num_primes(num)
    {
//      fprintf(stdout, "\nTrying to allocate a Primes object with size %zu\n", num_primes);
      primes = new size_t[num_primes];
//      fprintf(stdout, "\nprimes = %p\n", primes);
    }
    ~Primes()
    {
//      fprintf(stdout, "\nDeallocating the Primes object with size %zu\n", num_primes);
      delete[] primes;
    }

    ssize_t get_primes(void)
    {
      if (!num_primes or !primes) return -1;

      size_t i = 2, j, num = 0;
      size_t *primesptr = NULL;
      size_t *lastprime = primes;
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

    ssize_t get_num_primes(void)
    {
      if (!num_primes or !primes) return -1;

      size_t i, j, num = 0;
      size_t *primesptr = NULL;
      size_t *lastprime = primes;
      for (i = 2; i < num_primes; i++) {
        primesptr = primes;
        for (j = 0; j < num && i % (*primesptr); j++, primesptr++);
        if (j == num) {
          (*lastprime++) = i;
          ++num;
        }
      }
      return num;
    }
};

#endif /* #ifndef PRIMES_H */
