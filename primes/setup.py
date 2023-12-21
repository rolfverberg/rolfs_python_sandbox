from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        Extension(
            'get_primes',
            sources=['get_primes.pyx'],
            extra_compile_args=['-std=c99']))
)
