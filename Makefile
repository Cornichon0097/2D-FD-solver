# ================================= Variables ================================ #
# ---------------------------- Sources directories --------------------------- #
SRCDIR = src
BDGDIR = bindings
DOCDIR = doc

# ============================= Targets and rules ============================ #
# ------------------------------ Default target ------------------------------ #
all:
	$(MAKE) -C $(BDGDIR) install

.PHONY: all

# -------------------------------- Main rules -------------------------------- #
run: all
	python3 $(SRCDIR)/start.py

doc:
	doxygen Doxyfile

.PHONY: run \
        doc

# -------------------------------- Clean rules ------------------------------- #
clean:
	$(MAKE) -C $(BINDDIR) clean

distclean:
	$(MAKE) -C $(BINDDIR) distclean

maintainer-clean:
	$(MAKE) -C $(BINDDIR) maintainer-clean
	rm -rf $(DOCDIR)

.PHONY: clean \
        distclean \
        maintainer-clean
