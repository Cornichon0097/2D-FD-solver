# ================================= Variables ================================ #
# -------------------------------- directories ------------------------------- #
SRCDIR   = src
TESTSDIR = tests
BUILDDIR = build
OBJDIR   = $(BUILDDIR)/temp.linux-x86_64-cpython-311
LIBDIR   = $(BUILDDIR)/lib.linux-x86_64-cpython-311

# ----------------------------------- Files ---------------------------------- #
CUDA_TARGET = $(LIBDIR)/_solver.cpython-311-x86_64-linux-gnu.so
CUDA_OFILES = $(OBJDIR)/solver_wrap.o \
              $(OBJDIR)/src/solver.o \
              $(OBJDIR)/src/cuda_helper.o

# --------------------------------- Compilers -------------------------------- #
CXX      = g++
CXXFLAGS = -shared -Wl,-O1 -Wl,-Bsymbolic-functions -g -fwrapv -O2 \
           -L/usr/lib/x86_64-linux-gnu -L/usr/local/cuda-12.9/lib64

NVCC      = nvcc
NVCCFLAGS = --compiler-options -fPIC -shared -g -O2 -I./include/armanpy/ \
            -I$(SRCDIR) -I/home/cornichon/Documents/projects/prsa/venv/include \
            -I/usr/include/python3.11

# ============================= Targets and rules ============================ #
# ------------------------------ Default target ------------------------------ #
all: $(CUDA_TARGET)

$(CUDA_TARGET): $(CUDA_OFILES)
	$(CXX) $(CXXFLAGS) -o $@ $(CUDA_OFILES) -lm -lz -larmadillo -lcudart

$(OBJDIR)/solver_wrap.o: setup.py \
                         solver.i \
                         $(SRCDIR)/solver.cpp \
                         $(SRCDIR)/solver.h
	python3 setup.py build

$(OBJDIR)/src/cuda_helper.o: $(SRCDIR)/cuda_helper.cu \
                             $(SRCDIR)/cuda_helper.h
	$(NVCC) $(NVCCFLAGS) -o $@ -c $<

.PHONY: all

# ------------------------------- Install rule ------------------------------- #
install: all
	pip install .

.PHONY: install

# ------------------------------- Tests rules -------------------------------- #
test: $(TESTSDIR)/test_cuda_solver.cu \
      $(SRCDIR)/cuda_helper.cu
	$(NVCC) -I$(SRCDIR) -g -o $(BUILDDIR)/test_cuda_solver.out $^

run: install
	python3 tests/test_solver.py

.PHONY: test \
        run

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
