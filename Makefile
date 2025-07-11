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
	$(MAKE) -C $(BDGDIR) clean

distclean:
	$(MAKE) -C $(BDGDIR) distclean

maintainer-clean:
	$(MAKE) -C $(BDGDIR) maintainer-clean
	rm -rf $(DOCDIR)

.PHONY: clean \
        distclean \
        maintainer-clean
