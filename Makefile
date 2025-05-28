# ================================= Variables ================================ #
# ---------------------------- Sources directories --------------------------- #
SRCDIR   = src
TESTSDIR = tests
BINDDIR  = bindings
DOCDIR   = doc

# ============================= Targets and rules ============================ #
# ------------------------------ Default target ------------------------------ #
all: vti
	$(MAKE) -C $(BINDDIR) install

.PHONY: all

# ------------------------------- Tests rules -------------------------------- #
test:
	python3 tests/test_mongoDBConnection.py

.PHONY: test
# -------------------------------- Main rules -------------------------------- #
vti:
	mkdir -p $@

run: all
	python3 $(SRCDIR)/start.py

doc:
	doxygen Doxyfile

.PHONY: run \
        doc

# -------------------------------- Clean rules ------------------------------- #
clean:
	$(MAKE) -C $(BINDDIR) clean

distclean: clean
	$(MAKE) -C $(BINDDIR) distclean

maintainer-clean: distclean
	$(MAKE) -C $(BINDDIR) maintainer-clean
	rm -rf $(DOCDIR)

.PHONY: clean \
        distclean \
        maintainer-clean
