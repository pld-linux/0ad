#
# TODO: - use arch dependend compilers
#	- check licenses
#	- try to make it runnable by non-privileged users (sth wrong with boost?)
#	- fix problem with font finding
#
%define		svn_ver r8832
Summary:	Free, Open-Source, cross-platform RTS game of ancient warfare
Name:		0ad
Version:	%{svn_ver}
Release:	0.%{svn_ver}.1
License:	GPL v2+
Group:		X11/Applications/Games
Source0:	%{name}-%{version}-alpha-unix-build.tar.gz
# Source0-md5:	f38d660d039a37edebb2ea2f0eb6aa6d
URL:		http://wildfiregames.com/0ad/
BuildRequires:	DevIL-devel
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	enet-devel < 1.3.0
BuildRequires:	enet-devel >= 1.2.0
BuildRequires:	libogg-devel
BuildRequires:	libpng-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libxml2-devel
BuildRequires:	sed >= 4.0
BuildRequires:	wxGTK2-unicode-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
0 A.D. (pronounced "zero ey-dee") is a free, open-source,
cross-platform real-time strategy (RTS) game of ancient warfare. In
short, it is a historically-based war/economy game that allows players
to relive or rewrite the history of Western civilizations, focusing on
the years between 500 B.C. and 500 A.D. The project is highly
ambitious, involving state-of-the-art 3D graphics, detailed artwork,
sound, and a flexible and powerful custom-built game engine.

%prep
%setup -q -n %{name}

# force link with libboost_*.so not libboost_*-mt.so
%{__sed} -i 's,-mt,,g' build/premake/extern_libs.lua

# use wx-gtk2-unicode-config instead of wx-config
%{__sed} -i 's,wx-config,wx-gtk2-unicode-config,' build/premake/extern_libs.lua

%build
export CFLAGS="%{rpmcflags}"
export CPPFLAGS="%{rpmcxxflags}"
cd build/workspaces
./update-workspaces.sh \
	--verbose \
	--bindir %{_bindir} \
	--datadir %{_datadir}/%{name} \
	--libdir %{_libdir}/%{name}

cd gcc
%{__make} \
	CONFIG=Release

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/%{name},%{_desktopdir},%{_pixmapsdir}}

# binaries
cp -a build/resources/0ad.sh $RPM_BUILD_ROOT%{_bindir}/0ad
cp -a binaries/system/pyrogenesis $RPM_BUILD_ROOT%{_bindir}

# libraries
cp -a binaries/system/*.so $RPM_BUILD_ROOT%{_libdir}/%{name}

# menu icon
cp -a build/resources/0ad.desktop $RPM_BUILD_ROOT%{_desktopdir}
cp -a build/resources/0ad.png $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.txt
%attr(755,root,root) %{_bindir}/0ad
%attr(755,root,root) %{_bindir}/pyrogenesis
%dir %{_libdir}/0ad
%{_libdir}/0ad/*.so
%{_desktopdir}/0ad.desktop
%{_pixmapsdir}/0ad.png
