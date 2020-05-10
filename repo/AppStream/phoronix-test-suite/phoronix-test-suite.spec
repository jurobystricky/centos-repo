Summary:    A Comprehensive Linux Benchmarking System
Name:       phoronix-test-suite
Version:    9.6.0m1
Release:    9.6.0m1
License:    GPL

Group:      Utilities
URL: http://www.phoronix-test-suite.com/

Source: %{name}-%{version}.tar.gz

Requires: php-cli, php-xml, php-json, which

%description
@file_get_contents("pts-core/static/short-description.txt") . 

%global debug_package %{nil}

%prep
%setup -q

%build

%install
rm -rf %{buildroot}
./install-sh %{buildroot}/usr
sed -i 's|%buildroot||g' %buildroot%_bindir/phoronix-test-suite

%clean
rm -rf %{buildroot}

%files
%{_bindir}/phoronix-test-suite
%{_datadir}/phoronix-test-suite/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/doc/*
%{_datadir}/mime/*
%{_mandir}/man1/%{name}.1*
%config(noreplace) %{_sysconfdir}/bash_completion.d
%config(noreplace) %{_sysconfdir}/../usr/lib/systemd/system/*
