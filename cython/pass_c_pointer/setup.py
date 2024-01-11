from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        Extension(
            'memview_to_c',
            sources=['memview_to_c.pyx'],
            extra_compile_args=['-std=c99']))
)
