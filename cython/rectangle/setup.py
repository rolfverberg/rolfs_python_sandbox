from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        Extension(
            'rect',
            sources=['rect.pyx'],
            extra_compile_args=['-std=c99']))
)
