%define buildforkernels newest

# Define the kmod package name here.
%define kmod_name isgx

# If kversion isn't defined on the rpmbuild line, define it here.
%{!?kversion: %define kversion 4.18.0-151.el8}

Name:    %{kmod_name}-kmod
Version: 2.6
Release: 1%{?dist}
Group:   System Environment/Kernel
License: GPLv2
Summary: %{kmod_name} kernel module(s)
URL:     https://github.com/intel/linux-sgx-driver

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-build-%(%{__id_u} -n)
BuildRequires: %{_bindir}/kmodtool
BuildRequires: kernel = 4.18.0
BuildRequires: kernel-headers = 4.18.0
BuildRequires: kernel-devel = 4.18.0
BuildRequires: elfutils-libelf-devel


ExclusiveArch: i686 x86_64

Source0: sgx_driver_2.6.tar.gz

Patch0: rhel_8.patch

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provides the CentOS-5 bug-fixed %{kmod_name} kernel module (bug #1776).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -c -T -a 0

cd linux-sgx-driver-sgx_driver_2.6
%patch0 -p1

%build

cd linux-sgx-driver-sgx_driver_2.6
#export CFLAGS=-Wno-error
make CFLAGS="-Wno-incompatible-pointer-types" -C /lib/modules/4.18.0-187.el8.x86_64/build M=/builddir/build/BUILD/isgx-kmod-2.6/linux-sgx-driver-sgx_driver_2.6 modules

