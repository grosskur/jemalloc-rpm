Name:           jemalloc
Version:        2.0.1

Release:        3%{?dist}
Summary:        General-purpose scalable concurrent malloc implementation

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.canonware.com/jemalloc/
Source0:        http://www.canonware.com/download/jemalloc/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# Remove pprof, as it already exists in google-perftools
Patch0:         jemalloc-2.0.1.no_pprof.patch
# check for __s390__ as it's defined on both s390 and s390x
Patch1:         jemalloc-2.0.1-s390.patch

%description
General-purpose scalable concurrent malloc(3) implementation.
This distribution is the stand-alone "portable" implementation of %{name}.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Group:          Development/Libraries

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0
%patch1 -p1 -b .s390

%build
%configure
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# None of these in fedora
find %{buildroot}%{_libdir}/ -name '*.a' -exec rm -vf {} ';'


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{_libdir}/libjemalloc.so.*
%doc COPYING README VERSION

%files devel
%defattr(-,root,root,-)
%{_includedir}/jemalloc
%{_libdir}/libjemalloc.so
%{_mandir}/man3/jemalloc.3*

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%changelog
* Sat Dec 11 2010 Dan Horák <dan[at]danny.cz> - 2.0.1-3
- fix build on s390

* Thu Nov 18 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.0.1-2
- Added a patch that removes pprof, as it already exists in the
  google-perftools package
- Cosmetic fixes as requested in the package review (rhbz#653682)

* Mon Nov 15 2010 Ingvar Hagelund <ingvar@redpill-linpro.com> - 2.0.1-1
- First cut of an rpm distribution of jemalloc
