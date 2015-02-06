%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	A Nagios plugin to check SIP servers and devices
Name:		nagios-check_sip
Version:	1.2
Release:	7
License:	GPL
Group:		Networking/Other
URL:		http://www.bashton.com/content/nagiosplugins
Source0:	http://www.bashton.com/downloads/%{name}-%{version}.tar.gz
Requires:	nagios
BuildArch:  noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

%description
A Nagios plugin that will test a SIP server/device for availability and
response time.

%prep

%setup -q

%build

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_datadir}/nagios/plugins
install -m 755 check_sip %{buildroot}%{_datadir}/nagios/plugins

perl -pi -e 's|/usr/lib/nagios|%{_datadir}/nagios|' \
    %{buildroot}%{_datadir}/nagios/plugins/check_sip

install -d -m 755 %{buildroot}%{_sysconfdir}/nagios/plugins.d
cat > %{buildroot}%{_sysconfdir}/nagios/plugins.d/check_sip.cfg <<'EOF'
define command {
    command_name	check_sip
	command_line	%{_datadir}/nagios/plugins/check_sip -u $ARG1$ -H $HOSTADDRESS$ -w 5
}
EOF

%if %mdkversion < 200900
%post
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :

%postun
/sbin/service nagios condrestart > /dev/null 2>/dev/null || :
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README
%config(noreplace) %{_sysconfdir}/nagios/plugins.d/check_sip.cfg
%{_datadir}/nagios/plugins/check_sip


%changelog
* Sat Dec 11 2010 Oden Eriksson <oeriksson@mandriva.com> 1.2-6mdv2011.0
+ Revision: 620464
- the mass rebuild of 2010.0 packages

* Mon Sep 14 2009 Thierry Vignaud <tv@mandriva.org> 1.2-5mdv2010.0
+ Revision: 440227
- rebuild

* Mon Dec 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 1.2-4mdv2009.1
+ Revision: 314653
- now a noarch package
- use a herein document for configuration
- reply on filetrigger for reloading nagios

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.2-3mdv2009.0
+ Revision: 253532
- rebuild

  + Oden Eriksson <oeriksson@mandriva.com>
    - 1.2

* Tue Feb 19 2008 Oden Eriksson <oeriksson@mandriva.com> 1.1-1mdv2008.1
+ Revision: 173081
- 1.1

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue Apr 17 2007 Oden Eriksson <oeriksson@mandriva.com> 1.01-3mdv2008.0
+ Revision: 13796
- use the new /etc/nagios/plugins.d scandir


* Wed Nov 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1.01-2mdv2007.0
+ Revision: 84577
- Import nagios-check_sip

* Thu Aug 10 2006 Oden Eriksson <oeriksson@mandriva.com> 1.01-2mdk
- disable debug packages

* Thu Apr 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1.01-1mdk
- 1.01

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdk
- initial Mandriva package

