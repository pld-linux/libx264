%define		snap	20071008
%define		snaph	2245
%define		_rel	1
Summary:	H264 encoder library
Summary(pl.UTF-8):	Biblioteka kodująca H264
Name:		libx264
Version:	0.1.2
Release:	1.%{snap}_%{snaph}.%{_rel}
License:	GPL v2
Group:		Libraries
# unofficial, debianized/libtoolized packaging:
#Source0:	http://www.acarlab.com/misc-dnlds/%{name}-%{version}.tar.gz
# but it's too old, so use snapshots...
Source0:	ftp://ftp.videolan.org/pub/videolan/x264/snapshots/x264-snapshot-%{snap}-%{snaph}.tar.bz2
# Source0-md5:	b1747dd3c78e83c0d56832ac2e5b83df
Patch0:		%{name}-alpha.patch
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

%description -l pl.UTF-8
Biblioteka libx264 do kodowania w formacie obrazu H264.

%package devel
Summary:	Header files for x264 library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki x264
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for x264 library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki x264.

%package static
Summary:	Static x264 library
Summary(pl.UTF-8):	Statyczna biblioteka x264
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static x264 library.

%description static -l pl.UTF-8
Statyczna biblioteka x264.

%prep
%setup -q -n x264-snapshot-%{snap}-%{snaph}
sed -i 's:-O4::g' configure
%patch0 -p1

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
