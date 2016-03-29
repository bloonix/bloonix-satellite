CONFIG=Makefile.config

include $(CONFIG)

default: build

build:

	for file in \
		bin/bloonix-satellite \
		etc/bloonix/satellite/main.conf \
		etc/init/bloonix-satellite \
		etc/init/bloonix-satellite.service \
	; do \
		cp $$file.in $$file; \
		sed -i "s!@@PERL@@!$(PERL)!g" $$file; \
		sed -i "s!@@PREFIX@@!$(PREFIX)!g" $$file; \
		sed -i "s!@@CACHEDIR@@!$(CACHEDIR)!g" $$file; \
		sed -i "s!@@CONFDIR@@!$(CONFDIR)!g" $$file; \
		sed -i "s!@@RUNDIR@@!$(RUNDIR)!g" $$file; \
		sed -i "s!@@USRLIBDIR@@!$(USRLIBDIR)!" $$file; \
		sed -i "s!@@SRVDIR@@!$(SRVDIR)!g" $$file; \
		sed -i "s!@@LOGDIR@@!$(LOGDIR)!g" $$file; \
		sed -i "s!@@LIBDIR@@!$(LIBDIR)!g" $$file; \
	done;

test:

install:

	./install-sh -d -m 0750 $(LOGDIR)/bloonix;
	./install-sh -d -m 0755 $(LIBDIR)/bloonix;
	./install-sh -d -m 0755 $(RUNDIR)/bloonix;
	./install-sh -d -m 0755 $(USRLIBDIR)/bloonix;
	./install-sh -d -m 0755 $(PREFIX)/bin;
	./install-sh -d -m 0755 $(SRVDIR)/bloonix;
	./install-sh -d -m 0755 $(SRVDIR)/bloonix/satellite;
	./install-sh -d -m 0755 $(CONFDIR)/bloonix;
	./install-sh -d -m 0755 $(CONFDIR)/bloonix/satellite;

	for file in \
		bloonix-satellite \
		bloonix-init-satellite \
	; do \
		./install-sh -c -m 0755 bin/$$file $(PREFIX)/bin/$$file; \
	done;

	./install-sh -d -m 0755 $(USRLIBDIR)/bloonix/etc/satellite;
	./install-sh -c -m 0644 etc/bloonix/satellite/main.conf $(USRLIBDIR)/bloonix/etc/satellite/main.conf;

	./install-sh -d -m 0755 $(USRLIBDIR)/bloonix/etc/init.d;
	./install-sh -c -m 0755 etc/init/bloonix-satellite $(USRLIBDIR)/bloonix/etc/init.d/bloonix-satellite;

	./install-sh -d -m 0755 $(USRLIBDIR)/bloonix/etc/systemd;
	./install-sh -c -m 0755 etc/init/bloonix-satellite.service $(USRLIBDIR)/bloonix/etc/systemd/bloonix-satellite.service;

	if test "$(BUILDPKG)" = "0" ; then \
		if test -d /usr/lib/systemd ; then \
			./install-sh -d -m 0755 $(DESTDIR)/usr/lib/systemd/system/; \
			./install-sh -c -m 0644 etc/init/bloonix-satellite.service $(DESTDIR)/usr/lib/systemd/system/; \
			systemctl daemon-reload; \
		elif test -d /etc/init.d ; then \
			./install-sh -c -m 0755 etc/init/bloonix-satellite $(INITDIR)/bloonix-satellite; \
		fi; \
	fi;

clean:

