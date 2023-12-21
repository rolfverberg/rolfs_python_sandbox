from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    name='Fib',
    ext_modules = cythonize(
        Extension(
            'fib',
            sources=['fib.pyx'],
            extra_compile_args=['-std=c99']))
)
