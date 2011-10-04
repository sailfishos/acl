Summary: Access control list utilities
Name: acl
Version: 2.2.51
Release: 1
BuildRequires: libattr-devel >= 2.4.1
Source: http://download.savannah.gnu.org/releases/acl/acl-%{version}.src.tar.gz
# Make it install in $(DESTDIR)
Patch0: acl-2.2.49-build.patch
Patch1: acl-2.2.49-multilib.patch 
License: GPLv2
Group: System/Base
URL: http://savannah.nongnu.org/projects/acl
BuildRequires: gettext

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
Summary: Dynamic library for access control list support
License: LGPLv2.1
Group: System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary: Access control list static libraries and headers
License: LGPL
Group: Development/Libraries
Requires: libacl = %{version}-%{release}, libattr-devel

%description -n libacl-devel
This package contains static libraries and header files needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%setup -q
%patch0 -p1 -b .build
%patch1 -p1 -b .multi

%build
touch .census
#acl abuses libexecdir
autoconf
%configure --libdir=/%{_lib} --libexecdir=%{_libdir}
make LIBTOOL="libtool --tag=CC" %{?_smp_mflags}

%install
%make_install
make install-dev DESTDIR=$RPM_BUILD_ROOT
make install-lib DESTDIR=$RPM_BUILD_ROOT

# fix links to shared libs and permissions
rm -f $RPM_BUILD_ROOT/%{_libdir}/libacl.so
ln -sf ../../%{_lib}/libacl.so $RPM_BUILD_ROOT/%{_libdir}/libacl.so
chmod 0755 $RPM_BUILD_ROOT/%{_lib}/libacl.so.*.*.*

%find_lang %{name}
%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%lang_package


%docs_package

%files 
%defattr(-,root,root,-)
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl

%files -n libacl-devel
%defattr(-,root,root,-)
%{_defaultdocdir}/*
/%{_lib}/libacl.so
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_libdir}/libacl.*
%exclude /%{_libdir}/libacl.a
%exclude /%{_libdir}/libacl.la

%files -n libacl
%defattr(-,root,root,-)
/%{_lib}/libacl.so.*
