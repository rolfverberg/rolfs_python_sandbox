from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
#    name='Primes',
    ext_modules = cythonize(
        Extension(
            'primes',
            sources=['primes.pyx'],
            annotate=True))
#            annotate=True,
#            extra_compile_args=['-std=c99']))
)
