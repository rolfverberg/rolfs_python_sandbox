#ifndef COMPUTE_C_H
#define COMPUTE_C_H

#ifdef __cplusplus
extern "C" {
#endif

int clip(const int a, const int min_value, const int max_value);
void compute_in_c(const int* const array_1, const int* const array_2, int* const result,
    size_t array_size, int a, int b, int c);

#ifdef __cplusplus
}
#endif

#endif /* #ifndef COMPUTE_C_H */
