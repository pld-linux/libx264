Summary:	H264 encoder library
Summary(pl):	Biblioteka koduj±ca H264
Name:		libx264
Version:	0.1.2
Release:	1
License:	GPL v2
Group:		Libraries
# unofficial, debianized/libtoolized packaging;
# no official releases, only svn://svn.videolan.org/x264/trunk x264
Source0:	http://www.acarlab.com/misc-dnlds/%{name}-%{version}.tar.gz
# Source0-md5:	3bbaa669b3661d33030378f4919be576
Patch0:		%{name}-nasm.patch
Patch1:		%{name}-link.patch
URL:		http://developers.videolan.org/x264.html
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
libx264 library for encoding H264 video format.

%description -l pl
Biblioteka libx264 do kodowania w formacie obrazu H264.

%package devel
Summary:	Header files for x264 library
Summary(pl):	Pliki nag³ówkowe biblioteki x264
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for x264 library.

%description devel -l pl
Pliki nag³ówkowe biblioteki x264.

%package static
Summary:	Static x264 library
Summary(pl):	Statyczna biblioteka x264
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static x264 library.

%description static -l pl
Statyczna biblioteka x264.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS TODO
%attr(755,root,root) %{_bindir}/x264
%attr(755,root,root) %{_libdir}/libx264.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libx264.so
%{_libdir}/libx264.la
%{_includedir}/x264.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libx264.a
