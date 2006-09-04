Summary:	H264 encoder library
Summary(pl):	Biblioteka koduj±ca H264
Name:		libx264
Version:	0.1.2
%define	snap	20060828
%define	snaph	2245
Release:	1.%{snap}_%{snaph}.1
License:	GPL v2
Group:		Libraries
# unofficial, debianized/libtoolized packaging:
#Source0:	http://www.acarlab.com/misc-dnlds/%{name}-%{version}.tar.gz
# but it's too old, so use snapshots...
Source0:	ftp://ftp.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-%{snap}-%{snaph}.tar.bz2
# Source0-md5:	7c18e71f2821af69e66cae4095b9bce7
URL:		http://developers.videolan.org/x264.html
%ifarch %{ix86}
BuildRequires:	nasm
%endif
BuildRequires:	sed >= 4.0
%ifarch %{x8664}
BuildRequires:	yasm
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# encoder/macroblock.c breaks strict-aliasing rules
%define		specflags	-fno-strict-aliasing

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
sed -i 's:-O4::g' configure

%build
CC="%{__cc}" \
./configure \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--extra-cflags="%{rpmcflags}" \
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
