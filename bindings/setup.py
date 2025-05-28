from setuptools import setup, Extension

module1 = Extension('_solver',
                    include_dirs = ['./include/armanpy/'],
                    libraries = ['m', 'z', 'armadillo'],
                    sources = ['solver.i', 'solver.cpp'],
                    swig_opts = ["-c++", "-Wall", "-I.", "-I./include/armanpy/"])

setup(name = 'solver',
      py_modules = ['solver'],
      version = '1.0',
      description = 'This is a solver package',
      ext_modules = [module1])
