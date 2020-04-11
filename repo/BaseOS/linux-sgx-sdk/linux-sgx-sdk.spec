Name:    sgx-sdk
Version: 2.9
Release: 101.2%{?dist}
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

# prepare prebuilt binaries
tar -zxf %{_sourcedir}/optimized_libs_2.9.1.tar.gz -C .
tar -zxf %{_sourcedir}/prebuilt_ae_2.9.1.tar.gz -C .
tar -zxf %{_sourcedir}/as.ld.objdump.gold.r1.tar.gz -C .

%build
#
# On CentOS Stream, the default compiler is GCC8.4 which does not support
# mitigation flag -Wa,-mlfence-after-load=yes, so set target to sdk_no_mitigation
#
make sdk_no_mitigation DEBUG=1

%install
mkdir -p %{buildroot}/opt/intel/sgxsdk/

# Sample Code
cp -r SampleCode %{buildroot}/opt/intel/sgxsdk -fr

# bin
mkdir -p %{buildroot}/opt/intel/sgxsdk/bin/x64
cp -r build/linux/sgx_config_cpusvn %{buildroot}/opt/intel/sgxsdk/bin/x64
cp -r build/linux/sgx_edger8r %{buildroot}/opt/intel/sgxsdk/bin/x64
cp -r build/linux/sgx_encrypt %{buildroot}/opt/intel/sgxsdk/bin/x64
cp -r build/linux/sgx_sign %{buildroot}/opt/intel/sgxsdk/bin/x64

# lib64
mkdir -p %{buildroot}/opt/intel/sgxsdk/lib64
cp -r build/linux/* %{buildroot}/opt/intel/sgxsdk/lib64
rm %{buildroot}/opt/intel/sgxsdk/lib64/sgx_config_cpusvn
rm %{buildroot}/opt/intel/sgxsdk/lib64/sgx_edger8r
rm %{buildroot}/opt/intel/sgxsdk/lib64/sgx_encrypt
rm %{buildroot}/opt/intel/sgxsdk/lib64/sgx_sign

# include
cp common/inc %{buildroot}/opt/intel/sgxsdk/include -fr
mkdir -p %{buildroot}/opt/intel/sgxsdk/include/ipp
cp external/ippcp_internal/inc/*.h %{buildroot}/opt/intel/sgxsdk/include/ipp -fr
cp sdk/tlibcxx/include %{buildroot}/opt/intel/sgxsdk/include/libcxx -fr

# License
mkdir -p %{buildroot}/opt/intel/sgxsdk/licenses
cp License.txt %{buildroot}/opt/intel/sgxsdk/licenses

rm %{buildroot}/usr/lib/.build-id -fr

pathfix.py -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}/opt/intel/sgxsdk/

#
# TODO: still missing pkgconfig.pc files
#

%files
/opt/intel/sgxsdk/*