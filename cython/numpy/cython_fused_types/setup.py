from setuptools import Extension, setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize(
        Extension(
            'compute_fused_types',
            sources=['compute_fused_types.pyx'],
            extra_compile_args=['-std=c99']))
)
