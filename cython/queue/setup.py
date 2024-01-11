from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        Extension(
            'queue',
            sources=['queue.pyx'],
            extra_compile_args=['-std=c99']))
)
