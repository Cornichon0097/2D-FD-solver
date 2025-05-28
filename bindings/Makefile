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

# --------------------------------- Cuda rule -------------------------------- #
cuda: $(SRCDIR)/cuda_solver.cpp \
      $(SRCDIR)/solver.h \
      $(SRCDIR)/cuda_helper.cu \
      $(SRCDIR)/cuda_helper.h
	./scripts/setup_cuda.sh

.PHONY: cuda

# ------------------------------- Install rule ------------------------------- #
install: all
	pip install .

.PHONY: install

# ------------------------------- Install rule ------------------------------- #
run: install
	python3 tests/test_solver.py

.PHONY: run

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
