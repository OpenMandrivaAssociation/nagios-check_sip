%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	A Nagios plugin to check SIP servers and devices
Name:		nagios-check_sip
Version:	1.01
Release:	%mkrel 3
License:	GPL
Group:		Networking/Other
URL:		http://www.bashton.com/content/nagiosplugins
Source0:	http://www.bashton.com/downloads/%{name}-%{version}.tar.bz2
Source1:	check_sip.cfg
Requires:	nagios

%description
A Nagios plugin that will test a SIP server/device for availability and
response time.

%prep

%setup -q

cp %{SOURCE1} check_sip.cfg

# lib64 fix
perl -pi -e "s|/usr/lib|%{_libdir}|g" check_sip
perl -pi -e "s|_LIBDIR_|%{_libdir}|g" *.cfg

%build

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/nagios/plugins.d
install -d %{buildroot}%{_libdir}/nagios/plugins

install -m0755 check_sip %{buildroot}%{_libdir}/nagios/plugins/
install -m0644 *.cfg %{buildroot}%{_sysconfdir}/nagios/plugins.d/

%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_sip.cfg
%attr(0755,root,root) %{_libdir}/nagios/plugins/check_sip
