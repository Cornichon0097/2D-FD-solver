# ================================= Variables ================================ #
# -------------------------------- directories ------------------------------- #
SRCDIR   = src
TESTSDIR = tests

# ============================= Targets and rules ============================ #
# ------------------------------ Default target ------------------------------ #
all: $(SRCDIR)/solver.cpp \
     $(SRCDIR)/solver.h
	python3 setup.py build

.PHONY: all

# ------------------------------- Install rule ------------------------------- #
install: cuda
	pip install .

.PHONY: install

# --------------------------------- Cuda rule -------------------------------- #
cuda: all \
      $(SRCDIR)/cuda_helper.cu \
      $(SRCDIR)/cuda_helper.h
	nvcc --compiler-options -fPIC -shared -g -O2 -I./include/armanpy/ -I./src/ -I/home/cornichon/Documents/projects/prsa/venv/include -I/usr/include/python3.11 -c src/cuda_helper.cu -o build/temp.linux-x86_64-cpython-311/src/cuda_helper.o
	x86_64-linux-gnu-g++ -shared -Wl,-O1 -Wl,-Bsymbolic-functions -g -fwrapv -O2 build/temp.linux-x86_64-cpython-311/solver_wrap.o build/temp.linux-x86_64-cpython-311/src/cuda_solver.o build/temp.linux-x86_64-cpython-311/src/cuda_helper.o -L/usr/lib/x86_64-linux-gnu -lm -lz -larmadillo -L/usr/local/cuda-12.9/lib64 -lcudart -o build/lib.linux-x86_64-cpython-311/_solver.cpython-311-x86_64-linux-gnu.so

.PHONY: cuda

# -------------------------------- Style rule -------------------------------- #
style:
	astyle --project $(SRCDIR)/*

.PHONY: style

# -------------------------------- Clean rules ------------------------------- #
clean:
	python3 setup.py clean --all

distclean: clean
	rm -rf solver.egg-info

maintainer-clean: distclean
	rm -f solver.py solver_wrap.cpp

.PHONY: clean \
        distclean \
        maintainer-clean
