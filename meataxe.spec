Name:           meataxe
Version:        2.4.24
Release:        4%{?dist}
Summary:        Matrix representations over finite fields

Group:          Sciences/Mathematics
License:        GPLv2+
URL:            http://www.math.rwth-aachen.de/~MTX/
Source0:        http://www.math.rwth-aachen.de/~MTX/%{name}-%{version}.tar.gz
# These man pages were written by Jerry James <loganjerry@gmail.com> using
# text taken from the sources.  Therefore, these pages have the same copyright
# and license as the source files.
Source1:        %{name}-man.tar.xz
# This patch causes a shared library to be built instead of a static library,
# and to link all of the binaries against the shared library.  Upstream is
# not interested in building a shared library.
Patch0:         %{name}-shared.patch

BuildRequires:  doxygen
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description
The MeatAxe is a set of programs for working with matrix representations
over finite fields.  Permutation representations are supported to some
extent, too.

%package libs
Summary:        Library of matrix representations over finite fields
Group:          Development/Other

%description libs
This package contains the MeatAxe library, which provides functions for
working with matrix representations over finite fields.  Permutation
representations are supported to some extent, too.

%package devel
Summary:        Header files and libraries for MeatAxe development
Group:          Development/Other
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and library links for building
applications that use the MeatAxe library.

%prep
%setup -q -c
%setup -q -T -D -a 1
%patch0

# Set up the configuration
sed -e "s|^MTXLIB=.*|MTXLIB=%{_libdir}|" \
    -e "s|^MTXBIN=.*|MTXBIN=%{_bindir}|" \
    -e "s|^CFLAGS1=.*|CFLAGS1=-std=gnu99 $RPM_OPT_FLAGS|" \
    Makefile.conf.dist > Makefile.conf

# Let Doxygen find standard header files
sed -ri \
    "s|^(INCLUDE_PATH.*=)|\1 %{_includedir} `echo %{_libdir}/gcc/*/*/include`|" \
    etc/Doxyfile

# Let us see compiler warnings
sed -i 's|@\$(CC)|\$(CC)|' Makefile

%build
make %{?_smp_mflags} VERSION=%{version} LFLAGS1="$RPM_LD_FLAGS"
make %{?_smp_mflags} rebuild-doc

%install
# Install the binaries
mkdir -p $RPM_BUILD_ROOT%{_bindir}
install -m 0755 bin/* -p $RPM_BUILD_ROOT%{_bindir}
rm -f $RPM_BUILD_ROOT%{_bindir}/mk.dir

# Install the libraries
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp -dp tmp/libmtx.so* $RPM_BUILD_ROOT%{_libdir}
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libmtx.so.%{version}

# Install the header
mkdir -p $RPM_BUILD_ROOT%{_includedir}
cp -p src/meataxe.h $RPM_BUILD_ROOT%{_includedir}

# Install the man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cd man
for m in *.1; do
  sed "s/@VERSION@/%{version}/" $m > $RPM_BUILD_ROOT%{_mandir}/man1/$m
  touch -r $m $RPM_BUILD_ROOT%{_mandir}/man1/$m
done

%check
make check

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%{_bindir}/*
%{_mandir}/man1/*

%files libs
%doc COPYING README
%{_libdir}/libmtx.so.*

%files devel
%doc doc
%{_includedir}/meataxe.h
%{_libdir}/libmtx.so

%changelog
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 28 2012 Jerry James <loganjerry@gmail.com> - 2.4.24-2
- Enable verbose build
- Fix binary and library permissions

* Fri Jan  6 2012 Jerry James <loganjerry@gmail.com> - 2.4.24-1
- Initial RPM
