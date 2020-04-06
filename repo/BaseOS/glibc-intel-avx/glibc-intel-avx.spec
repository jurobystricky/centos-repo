%define glibcsrcdir glibc-2.28
%define glibcversion 2.28
%define glibcrelease 72%{?dist}.1
%define glibc_target x86_64-redhat-linux

Summary: The GNU libc libraries
Name: glibc-intel-avx
Version: %{glibcversion}
Release: %{glibcrelease}

License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv2+ with exceptions and BSD and Inner-Net and ISC and Public Domain and GFDL

URL: http://www.gnu.org/software/glibc/
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.xz
Source1: build-locale-archive.c
Source4: nscd.conf
Source7: nsswitch.conf
Source8: power6emul.c
Source9: bench.mk
Source10: glibc-bench-compare
Source11: SUPPORTED
Source12: ChangeLog.old

Patch2: glibc-fedora-nscd.patch
Patch3: glibc-rh697421.patch
Patch4: glibc-fedora-linux-tcsetattr.patch
Patch5: glibc-rh741105.patch
Patch6: glibc-fedora-localedef.patch
Patch7: glibc-fedora-nis-rh188246.patch
Patch8: glibc-fedora-manual-dircategory.patch
Patch9: glibc-rh827510.patch
Patch10: glibc-fedora-locarchive.patch
Patch11: glibc-fedora-streams-rh436349.patch
Patch12: glibc-rh819430.patch
Patch13: glibc-fedora-localedata-rh61908.patch
Patch14: glibc-fedora-__libc_multiple_libcs.patch
Patch15: glibc-rh1070416.patch
Patch16: glibc-nscd-sysconfig.patch
Patch17: glibc-cs-path.patch
Patch18: glibc-c-utf8-locale.patch
Patch23: glibc-python3.patch
Patch24: glibc-with-nonshared-cflags.patch
Patch25: glibc-asflags.patch
Patch27: glibc-rh1614253.patch
Patch28: glibc-rh1577365.patch
Patch29: glibc-rh1615781.patch
Patch30: glibc-rh1615784.patch
Patch31: glibc-rh1615790.patch
Patch32: glibc-rh1622675.patch
Patch33: glibc-rh1622678-1.patch
Patch34: glibc-rh1622678-2.patch
Patch35: glibc-rh1631293-1.patch
Patch36: glibc-rh1631293-2.patch
Patch37: glibc-rh1623536.patch
Patch38: glibc-rh1631722.patch
Patch39: glibc-rh1631730.patch
Patch40: glibc-rh1623536-2.patch
Patch41: glibc-rh1614979.patch
Patch42: glibc-rh1645593.patch
Patch43: glibc-rh1645596.patch
Patch44: glibc-rh1645604.patch
Patch45: glibc-rh1646379.patch
Patch46: glibc-rh1645601.patch
Patch52: glibc-rh1638523-1.patch
Patch47: glibc-rh1638523-2.patch
Patch48: glibc-rh1638523-3.patch
Patch49: glibc-rh1638523-4.patch
Patch50: glibc-rh1638523-5.patch
Patch51: glibc-rh1638523-6.patch
Patch53: glibc-rh1641982.patch
Patch54: glibc-rh1645597.patch
Patch55: glibc-rh1650560-1.patch
Patch56: glibc-rh1650560-2.patch
Patch57: glibc-rh1650563.patch
Patch58: glibc-rh1650566.patch
Patch59: glibc-rh1650571.patch
Patch60: glibc-rh1638520.patch
Patch61: glibc-rh1651274.patch
Patch62: glibc-rh1654010-1.patch
Patch63: glibc-rh1635779.patch
Patch64: glibc-rh1654010-2.patch
Patch65: glibc-rh1654010-3.patch
Patch66: glibc-rh1654010-4.patch
Patch67: glibc-rh1654010-5.patch
Patch68: glibc-rh1654010-6.patch
Patch69: glibc-rh1642094-1.patch
Patch70: glibc-rh1642094-2.patch
Patch71: glibc-rh1642094-3.patch
Patch72: glibc-rh1654872-1.patch
Patch73: glibc-rh1654872-2.patch
Patch74: glibc-rh1651283-1.patch
Patch75: glibc-rh1662843-1.patch
Patch76: glibc-rh1662843-2.patch
Patch77: glibc-rh1623537.patch
Patch78: glibc-rh1577438.patch
Patch79: glibc-rh1664408.patch
Patch80: glibc-rh1651742.patch
Patch81: glibc-rh1672773.patch
Patch82: glibc-rh1651283-2.patch
Patch83: glibc-rh1651283-3.patch
Patch84: glibc-rh1651283-4.patch
Patch85: glibc-rh1651283-5.patch
Patch86: glibc-rh1651283-6.patch
Patch87: glibc-rh1651283-7.patch
Patch88: glibc-rh1659293-1.patch
Patch89: glibc-rh1659293-2.patch
Patch90: glibc-rh1639343-1.patch
Patch91: glibc-rh1639343-2.patch
Patch92: glibc-rh1639343-3.patch
Patch93: glibc-rh1639343-4.patch
Patch94: glibc-rh1639343-5.patch
Patch95: glibc-rh1639343-6.patch
Patch96: glibc-rh1663035.patch
Patch97: glibc-rh1658901.patch
Patch98: glibc-rh1659512-1.patch
Patch99: glibc-rh1659512-2.patch
Patch100: glibc-rh1659438-1.patch
Patch101: glibc-rh1659438-2.patch
Patch102: glibc-rh1659438-3.patch
Patch103: glibc-rh1659438-4.patch
Patch104: glibc-rh1659438-5.patch
Patch105: glibc-rh1659438-6.patch
Patch106: glibc-rh1659438-7.patch
Patch107: glibc-rh1659438-8.patch
Patch108: glibc-rh1659438-9.patch
Patch109: glibc-rh1659438-10.patch
Patch110: glibc-rh1659438-11.patch
Patch111: glibc-rh1659438-12.patch
Patch112: glibc-rh1659438-13.patch
Patch113: glibc-rh1659438-14.patch
Patch114: glibc-rh1659438-15.patch
Patch115: glibc-rh1659438-16.patch
Patch116: glibc-rh1659438-17.patch
Patch117: glibc-rh1659438-18.patch
Patch118: glibc-rh1659438-19.patch
Patch119: glibc-rh1659438-20.patch
Patch120: glibc-rh1659438-21.patch
Patch121: glibc-rh1659438-22.patch
Patch122: glibc-rh1659438-23.patch
Patch123: glibc-rh1659438-24.patch
Patch124: glibc-rh1659438-25.patch
Patch125: glibc-rh1659438-26.patch
Patch126: glibc-rh1659438-27.patch
Patch127: glibc-rh1659438-28.patch
Patch128: glibc-rh1659438-29.patch
Patch129: glibc-rh1659438-30.patch
Patch130: glibc-rh1659438-31.patch
Patch131: glibc-rh1659438-32.patch
Patch132: glibc-rh1659438-33.patch
Patch133: glibc-rh1659438-34.patch
Patch134: glibc-rh1659438-35.patch
Patch135: glibc-rh1659438-36.patch
Patch136: glibc-rh1659438-37.patch
Patch137: glibc-rh1659438-38.patch
Patch138: glibc-rh1659438-39.patch
Patch139: glibc-rh1659438-40.patch
Patch140: glibc-rh1659438-41.patch
Patch141: glibc-rh1659438-42.patch
Patch142: glibc-rh1659438-43.patch
Patch143: glibc-rh1659438-44.patch
Patch144: glibc-rh1659438-45.patch
Patch145: glibc-rh1659438-46.patch
Patch146: glibc-rh1659438-47.patch
Patch147: glibc-rh1659438-48.patch
Patch148: glibc-rh1659438-49.patch
Patch149: glibc-rh1659438-50.patch
Patch150: glibc-rh1659438-51.patch
Patch151: glibc-rh1659438-52.patch
Patch152: glibc-rh1659438-53.patch
Patch153: glibc-rh1659438-54.patch
Patch154: glibc-rh1659438-55.patch
Patch155: glibc-rh1659438-56.patch
Patch156: glibc-rh1659438-57.patch
Patch157: glibc-rh1659438-58.patch
Patch158: glibc-rh1659438-59.patch
Patch159: glibc-rh1659438-60.patch
Patch160: glibc-rh1659438-61.patch
Patch161: glibc-rh1659438-62.patch
Patch162: glibc-rh1702539-1.patch
Patch163: glibc-rh1702539-2.patch
Patch164: glibc-rh1701605-1.patch
Patch165: glibc-rh1701605-2.patch
Patch166: glibc-rh1691528-1.patch
Patch167: glibc-rh1691528-2.patch
Patch168: glibc-rh1706777.patch
Patch169: glibc-rh1710478.patch
Patch170: glibc-rh1670043-1.patch
Patch171: glibc-rh1670043-2.patch
Patch172: glibc-rh1710894.patch
Patch173: glibc-rh1699194-1.patch
Patch174: glibc-rh1699194-2.patch
Patch175: glibc-rh1699194-3.patch
Patch176: glibc-rh1699194-4.patch
Patch177: glibc-rh1727241-1.patch
Patch178: glibc-rh1727241-2.patch
Patch179: glibc-rh1727241-3.patch
Patch180: glibc-rh1717438.patch
Patch181: glibc-rh1727152.patch
Patch182: glibc-rh1724975.patch
Patch183: glibc-rh1722215.patch
Patch184: glibc-rh1777797.patch
# Clear optimization patches
Patch185: mathlto.patch
#Patch186: 0001-x86-64-Remove-sysdeps-x86_64-fpu-s_sinf.S.patch
#Patch187: pause.patch
Patch188: gcc-8-fix.patch
Patch189: spin-smarter.patch
Patch190: nostackshrink.patch
Patch191: 0001-Compile-branred.c-with-mprefer-vector-width-128.patch
Patch192: 0001-Set-vector-width-and-alignment-to-fix-GCC-AVX-issue.patch
Patch193: 0001-Force-ffsll-to-be-64-bytes-aligned.patch

Requires(pre): basesystem

# Filter out all GLIBC_PRIVATE symbols since they are internal to
# the package and should not be examined by any other tool.
%global __filter_GLIBC_PRIVATE 1

# Disable the building of the debug package(s).
%define debug_package %{nil}

BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext
BuildRequires: procps-ng, util-linux, gawk
BuildRequires: systemtap-sdt-devel
BuildRequires: systemd
BuildRequires: python3 python3-devel

BuildRequires: gcc >= 8.2.1-3.4
BuildRequires: make >= 4.0
BuildRequires: bison >= 2.7
BuildRequires: binutils >= 2.30-51

%description
AVX2/AVX512 build with Intel optimizations for glibc.

%prep
%autosetup -n %{glibcsrcdir} -p1

%build

mkdir build-glibc-avx2
pushd build-glibc-avx2

export CFLAGS="-O3 -march=haswell -mtune=skylake -g2 -m64  -Wl,-z,max-page-size=0x1000"
export ASFLAGS="-D__AVX__=1 -D__AVX2__=1 -msse2avx -D__FMA__=1"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "

../configure \
    --prefix=/usr \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/bin \
    --libexecdir=/usr/lib64/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=/usr/lib64 \
    --localedir=/usr/share/locale \
    --infodir=/usr/share/info \
    --mandir=/usr/share/man \
    --enable-kernel=3.2 \
    --disable-profile \
    --without-selinux \
    --build=%{glibc_target} \
    --enable-bind-now  \
    --enable-tunables \
    --enable-systemtap \
    --enable-stack-protector=strong \
    --enable-cet \
    --disable-crypt \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/share/locale
make %{?_smp_mflags}
popd

mkdir build-glibc-avx512
pushd build-glibc-avx512

export CFLAGS="-O3 -march=skylake-avx512 -mtune=skylake-avx512 -g2 -m64  -Wl,-z,max-page-size=0x1000 -fPIC "
export ASFLAGS="-D__AVX__=1 -D__AVX2__=1 -msse2avx -D__FMA__=1"
unset LDFLAGS
export LDFLAGS="-Wl,-z,max-page-size=0x1000 "

../configure \
    --prefix=/usr \
    --exec_prefix=/usr \
    --bindir=/usr/bin \
    --sbindir=/usr/bin \
    --libexecdir=/usr/lib64/glibc \
    --datadir=/usr/share \
    --sysconfdir=%{_sysconfdir} \
    --sharedstatedir=%{_localstatedir}/lib \
    --localstatedir=%{_localstatedir} \
    --libdir=/usr/lib64 \
    --localedir=/usr/share/locale \
    --infodir=/usr/share/info \
    --mandir=/usr/share/man \
    --enable-kernel=3.2 \
    --disable-profile \
    --without-selinux \
    --enable-obsolete-rpc \
    --build=%{glibc_target} \
    --enable-bind-now  \
    --enable-tunables \
    --enable-stack-protector=strong \
    --enable-cet \
    libc_cv_slibdir=/usr/lib64 \
    libc_cv_complocaledir=/usr/share/locale

make %{?_smp_mflags}
popd

%install

pushd build-glibc-avx2
mkdir -p %{buildroot}/usr/lib64/haswell
cp math/libm.so %{buildroot}/usr/lib64/haswell/libm-2.28.so
cp mathvec/libmvec.so %{buildroot}/usr/lib64/haswell/libmvec-2.28.so
cp libc.so  %{buildroot}/usr/lib64/haswell/libc-2.28.so
ln -s libm-2.28.so %{buildroot}/usr/lib64/haswell/libm.so.6
ln -s libmvec-2.28.so %{buildroot}/usr/lib64/haswell/libmvec.so.1
ln -s libc-2.28.so  %{buildroot}/usr/lib64/haswell/libc.so.6
popd

pushd build-glibc-avx512
mkdir -p %{buildroot}/usr/lib64/haswell/avx512_1
cp math/libm.so %{buildroot}/usr/lib64/haswell/avx512_1/libm-2.28.so
cp mathvec/libmvec.so %{buildroot}/usr/lib64/haswell/avx512_1/libmvec-2.28.so
ln -s libm-2.28.so %{buildroot}/usr/lib64/haswell/avx512_1/libm.so.6
ln -s libmvec-2.28.so %{buildroot}/usr/lib64/haswell/avx512_1/libmvec.so.1
popd

%files
/usr/lib64/haswell/avx512_1/libm-2.28.so
/usr/lib64/haswell/avx512_1/libm.so.6
/usr/lib64/haswell/avx512_1/libmvec.so.1
/usr/lib64/haswell/avx512_1/libmvec-2.28.so
/usr/lib64/haswell/libc-2.28.so
/usr/lib64/haswell/libc.so.6
/usr/lib64/haswell/libm-2.28.so
/usr/lib64/haswell/libm.so.6
/usr/lib64/haswell/libmvec-2.28.so
/usr/lib64/haswell/libmvec.so.1
