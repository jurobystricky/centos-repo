%define kversion 4.18.0
%define krelease 147

Name:    sgx-kmod
Version: 2.6
Release: 1%{?dist}
Group:   System Environment/Kernel
License: GPLv2
Summary: SGX kernel module(s)
URL:     https://github.com/intel/linux-sgx-driver

BuildRequires: kernel = %{kversion}
BuildRequires: kernel-headers = %{kversion}
BuildRequires: kernel-devel = %{kversion}
BuildRequires: elfutils-libelf-devel

Requires: kernel = %{kversion}

Source0: sgx_driver_2.6.tar.gz

Patch0: rhel_8.patch

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provide SGX kernel driver based on CentOS Stream's kernel 4.18.0.

%prep
%setup -q -c -T -a 0

cd linux-sgx-driver-sgx_driver_%{version}
%patch0 -p1

%build

cd linux-sgx-driver-sgx_driver_%{version}
make -C /lib/modules/%{kversion}-%{krelease}.el8.x86_64/build \
    M=/builddir/build/BUILD/sgx-kmod-%{version}/linux-sgx-driver-sgx_driver_%{version} \
    modules

mkdir -p %{buildroot}/lib/modules/%{kversion}-%{krelease}.el8.x86_64/kernel/drivers/intel/sgx
cp isgx.ko %{buildroot}/lib/modules/%{kversion}-%{krelease}.el8.x86_64/kernel/drivers/intel/sgx
mkdir -p %{buildroot}/etc/modules-load.d
echo "isgx" >> %{buildroot}/etc/modules-load.d/sgx.conf

%files
/etc/modules-load.d/sgx.conf
/lib/modules/4.18.0-187.el8.x86_64/kernel/drivers/intel/sgx/isgx.ko