#
# Conditional build:
%bcond_with	tests		# build without tests

# TODO:
# - runtime Requires if any

%define		kdeframever	6.9
%define		qtver		5.15.2
%define		kfname		attica
Summary:	A Qt library that implements the Open Collaboration Services API
Name:		kf6-%{kfname}
Version:	6.9.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	1284908164349599c949e753de5a6d6d
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Network-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt6Test-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
#Obsoletes:	kf5-%{kfname} < %{version}
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6Network >= %{qtver}
Requires:	kf6-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Attica is a Qt library that implements the Open Collaboration Services
API version 1.6. The REST API is defined here:
<http://freedesktop.org/wiki/Specifications/open-collaboration-services-draft/>.

It grants easy access to the services such as querying information
about persons and contents. The library is used in KNewStuff3 as
content provider. In order to integrate with KDE's Plasma Desktop, a
platform plugin exists in kdebase.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
#Obsoletes:	kf5-%{kfname}-devel < %{version}
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qtver}
Requires:	Qt6Network-devel >= %{qtver}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS README.md
%attr(755,root,root) %{_libdir}/libKF6Attica.so.*.*.*
%ghost %{_libdir}/libKF6Attica.so.6
%{_datadir}/qlogging-categories6/attica.categories
%{_datadir}/qlogging-categories6/attica.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6Attica.so
%{_includedir}/KF6/Attica
%{_libdir}/cmake/KF6Attica
%{_pkgconfigdir}/KF6Attica.pc
