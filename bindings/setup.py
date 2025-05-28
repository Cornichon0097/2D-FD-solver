from setuptools import setup, Extension

extension_module = Extension('_solver',
      include_dirs = ['./include/armanpy/', 'src/'],
      libraries = ['m', 'z', 'armadillo'],
      sources = ['solver.i', 'src/solver.cpp'],
      swig_opts = ["-c++", "-Wall", "-I./include/armanpy/", "-I./src/",])

setup(name = 'solver',
      py_modules = ['solver'],
      version = '1.0',
      description = '2D-FD solevr',
      ext_modules = [extension_module])
