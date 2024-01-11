#ifndef GET_PRIMES_H
#define GET_PRIMES_H

#ifdef __cplusplus
extern "C" {
#endif

int get_primes(int num_primes, int *primes);
int get_num_primes(int num, int *primes);
int* alloc_primes(int num_primes);
void free_primes(int *primes);

#ifdef __cplusplus
}
#endif

#endif /* #ifndef GET_PRIMES_H */

