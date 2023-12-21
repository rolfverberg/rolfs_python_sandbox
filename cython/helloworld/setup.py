from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    name='Helloworld',
    ext_modules = cythonize(
        Extension(
            'helloworld',
            sources=['helloworld.pyx'],
            extra_compile_args=['-std=c99']))
)
