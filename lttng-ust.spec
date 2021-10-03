%define _disable_ld_no_undefined 1

%define major 0
%define ctl_major 5
%define libname %mklibname lttng-ust %major
%define devname %mklibname -d lttng-ust

Name:		lttng-ust
Version:	2.13.0
Release:	1
License:	LGPLv2 and GPLv2 and MIT
Group:		Development/C
Summary:	LTTng Userspace Tracer library
URL:		http://lttng.org
Source0:	http://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
Patch0:         lttng-gen-tp-shebang.patch
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(liburcu)
BuildRequires:	pkgconfig(numa)

%description
This library may be used by user space applications to generate
tracepoints using LTTng.

%libpackage lttng-ust-ctl %{ctl_major}

%package -n %{libname}
Summary:	LTTng Userspace Tracer library
Group:		Development/C

%description -n %{libname}
This library provides support for developing programs using
LTTng userspace tracing

%package -n %{devname}
Summary:	LTTng Userspace Tracer library headers and development files
Group:		Development/C
Provides:	lttng-ust-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Requires:	%mklibname lttng-ust-ctl %{ctl_major}
Requires:	pkgconfig(liburcu)

%description -n %{devname}
This library provides support for developing programs using
LTTng userspace tracing

%prep
%autosetup -p1
sed -i -e '/SUBDIRS/s:examples::' doc/Makefile.am

%build
export CC=gcc
export CXX=g++
#Reinitialize libtool with the fedora version to remove Rpath
libtoolize -cvfi
autoreconf -vif
%configure --docdir=%{_docdir}/%{name} --disable-static
%make_build V=1

%install
%make_install
rm -vf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_docdir}/%{name}

%files
%{_mandir}/man3/lttng-ust.3.*
%{_mandir}/man3/lttng-ust-cyg-profile.3.*
%{_mandir}/man3/lttng-ust-dl.3.*
%{_mandir}/man3/*trace*.3.*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_bindir}/lttng-gen-tp
%{_mandir}/man1/lttng-gen-tp.1.*
%{_prefix}/include/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ust*.pc
