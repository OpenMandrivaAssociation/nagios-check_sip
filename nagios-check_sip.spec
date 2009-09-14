%define _enable_debug_packages	%{nil}
%define debug_package		%{nil}

Summary:	A Nagios plugin to check SIP servers and devices
Name:		nagios-check_sip
Version:	1.2
Release:	%mkrel 5
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
