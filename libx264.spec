#
# Conditional build:
%bcond_with	bootstrap	# no ffmpeg/gpac support in x264 utility
%bcond_without	asm		# disable asm
%bcond_without	lsmash		# lsmash for MP4 (preferred over gpac)

%ifnarch %{ix86} %{x8664} aarch64
%undefine	with_asm
%endif

%define		rel	1
%define		snap	20191217
%define		snaph	2245
Summary:	H264 encoder library
Summary(pl.UTF-8):	Biblioteka kodująca H264
Name:		libx264
Version:	0.1.3
Release:	1.%{snap}_%{snaph}.%{rel}
License:	GPL v2+
Group:		Libraries
# still no releases, use snapshots
# for further changes see: https://code.videolan.org/videolan/x264/
Source0:	https://download.videolan.org/videolan/x264/snapshots/x264-snapshot-%{snap}-%{snaph}.tar.bz2
# Source0-md5:	6d6b7b49518ddfd42c4e3577b5242b31
Patch0:		%{name}-alpha.patch
Patch1:		altivec-no-vand.patch
Patch2:		%{name}-gpac.patch
Patch3:		x32.patch
URL:		http://www.videolan.org/developers/x264.html
%ifarch %{ix86} %{x8664}
%{?with_asm:BuildRequires:	nasm >= 2.13}
%endif
BuildRequires:	pkgconfig
%if %{without bootstrap}
# which version exactly???
# for full x264 CLI utility functionality it wants:
# libswscale >= 0.9.0 (in pkgconfig file)
# libav{format,codec,util} from ffmpeg >= r21854
BuildRequires:	ffmpeg-devel >= 0.7.1
BuildRequires:	ffms2-devel >= 2.21
# gpac >= 2007-06-21
%{!?with_lsmash:BuildRequires:	gpac-devel >= 0.5.0-3}
%{?with_lsmash:BuildRequires:	l-smash-devel >= 1.5}
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

%package -n x264
Summary:	x264 CLI decoder
Summary(pl.UTF-8):	Dekoder x264 działający z linii poleceń
Group:		Applications/Multimedia
Requires:	%{name} = %{version}-%{release}
%if %{without bootstrap}
Requires:	ffms2 >= 2.21
%if %{with lsmash}
Requires:	l-smash >= 1.5
%else
Requires:	gpac >= 0.5.0-3
%endif
%endif

%description -n x264
x264 CLI decoder.

%description -n x264 -l pl.UTF-8
Dekoder x264 działający z linii poleceń.

%prep
%setup -q -n x264-snapshot-%{snap}-%{snaph}
%patch0 -p1
%if "%{pld_release}" == "ac"
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1

%build
CC="%{__cc}" \
./configure \
	--host=%{_target_platform} \
	--prefix=%{_prefix} \
	--exec-prefix=%{_prefix} \
	--bindir=%{_bindir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--extra-cflags="%{rpmcflags}" \
	%{!?with_asm:--disable-asm} \
	--enable-pic \
	--enable-shared \
	--enable-static

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
%attr(755,root,root) %{_libdir}/libx264.so.157

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libx264.so
%{_includedir}/x264.h
%{_includedir}/x264_config.h
%{_pkgconfigdir}/x264.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libx264.a

%files -n x264
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/x264
