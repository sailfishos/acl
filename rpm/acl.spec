Summary: Access control list utilities
Name: acl
Version: 2.3.1
Release: 1
BuildRequires: gawk
BuildRequires: gettext
BuildRequires: libattr-devel
BuildRequires: libtool
Requires: libacl = %{version}-%{release}
Source: https://download-mirror.savannah.gnu.org/releases/acl/acl-%{version}.tar.gz

License: GPLv2+
URL: https://savannah.nongnu.org/projects/acl

%description
This package contains the getfacl and setfacl utilities needed for
manipulating access control lists.

%package -n libacl
Summary: Dynamic library for access control list support
License: LGPLv2+
Conflicts: filesystem < 3

%description -n libacl
This package contains the libacl.so dynamic library which contains
the POSIX 1003.1e draft standard 17 functions for manipulating access
control lists.

%package -n libacl-devel
Summary: Files needed for building programs with libacl
License: LGPLv2+
Requires: libacl = %{version}-%{release}, libattr-devel

%description -n libacl-devel
This package contains header files and documentation needed to develop
programs which make use of the access control list programming interface
defined in POSIX 1003.1e draft standard 17.

%prep
%setup -q -n %{name}-%{version}/%{name}

%build
./autogen.sh
%configure --disable-static --libexecdir=%{_libdir}

# uncomment to turn on optimizations
# sed -i 's/-O2/-O0/' libtool include/builddefs
# unset CFLAGS

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT

# get rid of libacl.a and libacl.la
rm -f $RPM_BUILD_ROOT%{_libdir}/libacl.a
rm -f $RPM_BUILD_ROOT%{_libdir}/libacl.la

chmod 0755 $RPM_BUILD_ROOT/%{_libdir}/libacl.so.*.*.*

# drop already installed documentation, we will use an RPM macro to install it
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}*

%find_lang %{name}

%post -n libacl -p /sbin/ldconfig

%postun -n libacl -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%license doc/COPYING*
%{_bindir}/chacl
%{_bindir}/getfacl
%{_bindir}/setfacl

%files -n libacl-devel
%defattr(-,root,root,-)
%{_libdir}/libacl.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/acl
%{_includedir}/sys/acl.h
%{_mandir}/man1/chacl.1*
%{_mandir}/man1/getfacl.1*
%{_mandir}/man1/setfacl.1*
%{_mandir}/man3/acl_*
%{_mandir}/man5/acl.5*

%files -n libacl
%defattr(-,root,root,-)
%license doc/COPYING.LGPL
%{_libdir}/libacl.so.*
