%global major 0
%define libname %mklibname lttng-ust %major
%define devname %mklibname -d lttng-ust

Name:           lttng-ust
Version:        2.8.1
Release:        1
License:        LGPLv2 and GPLv2 and MIT
Group:          Development/C
Summary:        LTTng Userspace Tracer library
URL:            http://lttng.org
Source0:        http://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2

BuildRequires:	pkgconfig(uuid)
BuildRequires:  pkgconfig(liburcu)

%description
This library may be used by user space applications to generate
tracepoints using LTTng.

%package -n %{libname}
Summary:        LTTng Userspace Tracer library
Group:          Development/C

%description -n %{libname}
This library provides support for developing programs using
LTTng userspace tracing

%package -n %{devname}
Summary:        LTTng Userspace Tracer library headers and development files
Group:          Development/C
Provides:       lttng-ust-devel = %{version}-%{release}
Requires:       %{libname}%{?_isa} = %{version}-%{release}
Requires:       userspace-rcu-devel

%description -n %{devname}
This library provides support for developing programs using
LTTng userspace tracing

%prep
%setup -q
sed -i -e '/SUBDIRS/s:examples::' doc/Makefile.am

%build
#Reinitialize libtool with the fedora version to remove Rpath
libtoolize -cvfi
autoreconf -vif
%configure --docdir=%{_docdir}/%{name} --disable-static
# --with-java-jdk
# Java support was disabled in lttng-ust's stable-2.0 branch upstream in
# http://git.lttng.org/?p=lttng-ust.git;a=commit;h=655a0d112540df3001f9823cd3b331b8254eb2aa
# We can revisit enabling this when the next major version is released.

%make V=1

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_libdir}/*.la

%files
%{_mandir}/man3/lttng-ust.3.*
%{_mandir}/man3/lttng-ust-cyg-profile.3.*
%{_mandir}/man3/lttng-ust-dl.3.*
%{_mandir}/man3/*trace*.3.*
%dir %{_docdir}/%{name}
%{_docdir}/%{name}/ChangeLog
%{_docdir}/%{name}/README.md
%{_docdir}/%{name}/java-agent.txt

%files -n %libname
%{_libdir}/*.so.*

%files -n %devname
%{_bindir}/lttng-gen-tp
%{_mandir}/man1/lttng-gen-tp.1.*
%{_prefix}/include/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ust*.pc
