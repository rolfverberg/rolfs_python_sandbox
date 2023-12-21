from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
#    name='Primes',
    ext_modules = cythonize(
        Extension(
            'primes',
            sources=['primes.pyx', 'primes_python_compiled.py'],
            annotate=True,
            extra_compile_args=['-std=c99']))
)
