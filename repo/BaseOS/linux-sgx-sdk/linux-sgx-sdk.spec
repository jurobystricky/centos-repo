Name:    sgx-sdk
Version: 2.9
Release: 1%{?dist}
License: GPLv2
Summary: SGX SDK
URL:     https://github.com/intel/linux-sgx

BuildRequires: git wget autoconf automake libtool cmake
BuildRequires: ocaml ocaml-ocamlbuild
BuildRequires: openssl-devel libcurl-devel protobuf-devel
BuildRequires: /usr/bin/pathfix.py

Source0: sgx_%{version}.tar.gz

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
This package provide SGX kernel driver based on CentOS Stream's kernel 4.18.0.

%prep
%setup -q -n linux-sgx-sgx_%{version}

%build
./download_prebuilt.sh
make sdk_no_mitigation DEBUG=1

%install
mkdir -p %{buildroot}/opt/sgxsdk
cp -r build/linux/* %{buildroot}/opt/sgxsdk
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}/opt/sgxsdk/

%files
/opt/sgxsdk/*