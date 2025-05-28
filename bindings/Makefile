# ================================= Variables ================================ #
# -------------------------------- directories ------------------------------- #
TESTSDIR = tests
OBJDIR   = obj
BINDIR   = bin

# --------------------------------- Compiler --------------------------------- #
CXX      = g++
CXXFLAGS = -g -O2 -std=c++11 -Wall -Wextra -Werror

# ---------------------------------- Linker ---------------------------------- #
LD      = g++
LDFLAGS = #-L$(ARMADILLODIR)

# ----------------------------------- Files ---------------------------------- #
TARGET = $(BINDIR)/test_solver.out

OFILES = $(OBJDIR)/solver.o \
         $(OBJDIR)/test_solver.o

# ============================= Targets and rules ============================ #
# ------------------------------ Default target ------------------------------ #
all: $(TARGET) #bindings

.PHONY: all

# ------------------------------ Python bindings ----------------------------- #
bindings: solver.cpp \
          solver.h
	python3 setup.py build

install: bindings
	python3 setup.py install --user

test: install
	python3 test.py

.PHONY: bindings \
        install \
        test

# ----------------------------- Directories rules ---------------------------- #
$(OBJDIR):
	mkdir -p $@

$(BINDIR):
	mkdir -p $@

# ------------------------------- Target rule -------------------------------- #
$(TARGET): $(OFILES) \
           $(BINDIR)
	$(LD) $(LDFLAGS) -o $@ $(OFILES) -larmadillo

$(OBJDIR)/solver.o: solver.cpp \
                    solver.h \
                    $(OBJDIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $<

$(OBJDIR)/test_solver.o: $(TESTSDIR)/test_solver.cpp \
                         $(OBJDIR)
	$(CXX) $(CXXFLAGS) -o $@ -c $<

$(TESTSDIR)/test_solver.cpp : $(TESTSDIR)/test_solver.h
	cxxtestgen --error-printer -o $@ $<

# -------------------------------- Main rules -------------------------------- #
style:
	astyle --project solver.cpp solver.h $(TESTSDIR)/test_solver.h

run: $(TARGET)
	./$<

.PHONY: style \
        run

# -------------------------------- Clean rules ------------------------------- #
clean:
	rm -f $(TARGET) $(OFILES)

distclean: clean
	python3 setup.py clean --all

maintainer-clean: distclean
	rm -f $(TESTSDIR)/test_solver.cpp solver.py solver_wrap.cpp

.PHONY: clean \
        distclean \
        maintainer-clean
