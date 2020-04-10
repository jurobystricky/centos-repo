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
%undefine _disable_source_fetch
Source1: https://download.01.org/intel-sgx/sgx-linux/2.9.1/optimized_libs_2.9.1.tar.gz
Source2: https://download.01.org/intel-sgx/sgx-linux/2.9.1/prebuilt_ae_2.9.1.tar.gz
Source3: https://download.01.org/intel-sgx/sgx-linux/2.9.1/as.ld.objdump.gold.r1.tar.gz
Source4: https://download.01.org/intel-sgx/sgx-linux/2.9.1/SHA256SUM_prebuilt_2.9.1.txt

# Disable the building of the debug package(s).
%define debug_package %{nil}

%description
SGX user space SDK.

%prep
%setup -q -n linux-sgx-sgx_%{version}

pushd %{_sourcedir}
sha256sum -c SHA256SUM_prebuilt_2.9.1.txt
popd

%build
tar -zxf %{_sourcedir}/optimized_libs_2.9.1.tar.gz -C .
tar -zxf %{_sourcedir}/prebuilt_ae_2.9.1.tar.gz -C .
tar -zxf %{_sourcedir}/as.ld.objdump.gold.r1.tar.gz -C .

#
# On CentOS Stream, the default compiler is GCC8.4 which does not support
# mitigation flag -Wa,-mlfence-after-load=yes, so set target to sdk_no_mitigation
#
make sdk_no_mitigation DEBUG=1

%install
mkdir -p %{buildroot}/opt/intel/sgxsdk
cp -r build/linux/* %{buildroot}/opt/intel/sgxsdk
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}/opt/intel/sgxsdk/

%files
/opt/intel/sgxsdk/*