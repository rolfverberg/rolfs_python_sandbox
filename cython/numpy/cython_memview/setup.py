from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        Extension(
            'compute_memview',
            sources=['compute_memview.pyx'],
            extra_compile_args=['-std=c99']))
)
