Summary: Bloonix satellite daemon
Name: bloonix-satellite
Version: 0.6
Release: 1%{dist}
License: GPLv3
Group: Utilities/System
Distribution: RHEL and CentOS

Packager: Jonny Schulz <js@bloonix.de>
Vendor: Bloonix

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Source0: http://download.bloonix.de/sources/%{name}-%{version}.tar.gz
Requires: bloonix-core
Requires: bloonix-plugins-basic
AutoReqProv: no

%description
bloonix-satellite provides a simple satellite server.

%define with_systemd 0
%define initdir %{_sysconfdir}/init.d
%define mandir8 %{_mandir}/man8
%define docdir %{_docdir}/%{name}-%{version}
%define blxdir /usr/lib/bloonix
%define confdir /usr/lib/bloonix/etc/bloonix
%define logdir /var/log/bloonix
%define rundir /var/run/bloonix

%prep
%setup -q -n %{name}-%{version}

%build
%{__perl} Configure.PL --prefix /usr --build-package
%{__make}

%install
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
mkdir -p ${RPM_BUILD_ROOT}%{docdir}
install -d -m 0750 ${RPM_BUILD_ROOT}%{logdir}
install -d -m 0750 ${RPM_BUILD_ROOT}%{rundir}
install -c -m 0444 LICENSE ${RPM_BUILD_ROOT}%{docdir}/
install -c -m 0444 ChangeLog ${RPM_BUILD_ROOT}%{docdir}/

%if 0%{?with_systemd}
install -p -D -m 0644 %{buildroot}%{blxdir}/etc/systemd/bloonix-satellite.service %{buildroot}%{_unitdir}/bloonix-satellite.service
%else
install -p -D -m 0755 %{buildroot}%{blxdir}/etc/init.d/bloonix-satellite %{buildroot}%{initdir}/bloonix-satellite
%endif

%post
/usr/bin/bloonix-init-satellite
%if 0%{?with_systemd}
%systemd_post bloonix-satellite.service
systemctl condrestart bloonix-satellite.service
%else
/sbin/chkconfig --add bloonix-satellite
/sbin/service bloonix-satellite condrestart &>/dev/null
%endif

%preun
%if 0%{?with_systemd}
%systemd_preun bloonix-satellite.service
%else
if [ $1 -eq 0 ]; then
    /sbin/service bloonix-satellite stop &>/dev/null || :
    /sbin/chkconfig --del bloonix-satellite
fi
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)

%dir %attr(0755, root, root) %{blxdir}
%dir %attr(0755, root, root) %{blxdir}/etc
%dir %attr(0755, root, root) %{blxdir}/etc/satellite
%{blxdir}/etc/satellite/main.conf
%dir %attr(0755, root, root) %{blxdir}/etc/systemd
%{blxdir}/etc/systemd/bloonix-satellite.service
%dir %attr(0755, root, root) %{blxdir}/etc/init.d
%{blxdir}/etc/init.d/bloonix-satellite
%dir %attr(0750, bloonix, bloonix) %{logdir}
%dir %attr(0750, bloonix, bloonix) %{rundir}

%{_bindir}/bloonix-satellite
%{_bindir}/bloonix-init-satellite

%if 0%{?with_systemd}
%{_unitdir}/bloonix-satellite.service
%else
%{initdir}/bloonix-satellite
%endif

%dir %attr(0755, root, root) %{docdir}
%doc %attr(0444, root, root) %{docdir}/ChangeLog
%doc %attr(0444, root, root) %{docdir}/LICENSE

%changelog
* Tue Aug 18 2015 Jonny Schulz <js@bloonix.de> - 0.6-1
  Fixed %preun section in spec file.
* Sun Aug 16 2015 Jonny Schulz <js@bloonix.de> - 0.5-1
- Kicked dependency bloonix-agent.
* Mon Jun 22 2015 Jonny Schulz <js@bloonix.de> - 0.4-1
- Fixed typo ckeck-pop3 -> check-pop3.
* Sun Jun 21 2015 Jonny Schulz <js@bloonix.de> - 0.3-1
- Added check-ftp to the list of allowed checks.
* Sun Apr 19 2015 Jonny Schulz <js@bloonix.de> - 0.2-1
- Fixed replacement of @@LIBDIR@@.
* Wed Apr 15 2015 Jonny Schulz <js@bloonix.de> - 0.1-1
- Initial release.
