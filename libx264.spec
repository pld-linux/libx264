Summary:	H264 encoder library
Summary(pl):	Biblioteka koduj±ca H264
Name:		libx264
Version:	0.1.2
%define	snap	20060430
%define	snaph	2245
Release:	0.%{snap}_%{snaph}.1
License:	GPL v2
Group:		Libraries
# unofficial, debianized/libtoolized packaging:
#Source0:	http://www.acarlab.com/misc-dnlds/%{name}-%{version}.tar.gz
# but it's too old, so use snapshots...
Source0:	ftp://ftp.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-%{snap}-%{snaph}.tar.bz2
# Source0-md5:	667c760dda91e9a3f50186d4676b5d5a
#Patch0:		%{name}-acam.patch
Patch1:		%{name}-liblink.patch
URL:		http://developers.videolan.org/x264.html
BuildRequires:	autoconf >= 2.53
BuildRequires:	automake
BuildRequires:	libtool
%ifarch %{ix86}
BuildRequires:	nasm
%endif
%ifarch %{x8664}
#BuildRequires:	yasm
%endif
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
%setup -q -n x264-snapshot-%{snap}-%{snaph}
#%patch0 -p1
%patch1 -p0

%build
##%{__libtoolize}
##%{__aclocal}
##%{__autoconf}
##%{__autoheader}
##%{__automake}
%configure \
    --enable-shared
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
%doc AUTHORS
%attr(755,root,root) %{_bindir}/x264
%attr(755,root,root) %{_libdir}/libx264.so.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libx264.so
%{_includedir}/x264.h
%{_pkgconfigdir}/x264.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libx264.a
