# ================================= Variables ================================ #
# -------------------------------- directories ------------------------------- #
SRCDIR   = src
TESTDIR = test

# ============================= Targets and rules ============================ #
# ------------------------------ Default target ------------------------------ #
all: $(SRCDIR)/solver.cpp \
     $(SRCDIR)/solver.h
	python3 setup.py build

.PHONY: all

# ------------------------------- Install rule ------------------------------- #
install: all
	pip install .

.PHONY: install

# -------------------------------- Tests rule -------------------------------- #
test: install
	python3 ${TESTDIR}/test_solver.py

.PHONY: test

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
