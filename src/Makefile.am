SUBDIRS = keepUp

bin_SCRIPTS = KeepUp
CLEANFILES = $(bin_SCRIPT)
EXTRA_DIST = KeepUp.in

do_subs = sed -e 's,[@]pythondir[@],$(pythondir),g' \
              -e 's,[@]PACKAGE[@],$(PACKAGE),g' \
              -e 's,[@]VERSION[@],$(VERSION),g' \
	      -e 's,[@]datadir[@],${datadir},g'

KeepUp: KeepUp.in Makefile
	$(do_subs) < $(srcdir)/KeepUp.in > KeepUp
	chmod +x KeepUp
