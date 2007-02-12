%define		mod_name	fcgid
%define 	apxs		/usr/sbin/apxs
Summary:	A binary compatibility alternative to Apache module mod_fastcgi
Summary(pl.UTF-8):   Binarnie kompatybilna alternatywa dla modułu Apache'a mod_fastcgi
Name:		apache-mod_%{mod_name}
Version:	1.03
Release:	3
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://fastcgi.coremail.cn/mod_%{mod_name}.%{version}.tar.gz
# Source0-md5:	dbcd5c96f8d6c6fcb7471abf527d176f
Source1:	%{name}.conf
Patch0:		%{name}-apr-status-is-success.patch
Patch1:		%{name}-apache.patch
URL:		http://fastcgi.coremail.cn/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
A binary compatibility alternative to Apache module mod_fastcgi.
mod_fcgid has a new process management strategy, which concentrates on
reducing the number of fastcgi server, and kick out the corrupt
fastcgi server as soon as possible.

%description -l pl.UTF-8
Binarnie kompatybilna alternatywa dla modułu Apache'a mod_fastcgi.
mod_fcgid to nowa strategia zarządzania procesami, koncentrująca się
na redukcji liczby serwerów fastcgi i usuwaniu uszkodzonych serwerów
fastcgi najszybciej jak to możliwe.

%prep
%setup -q -n mod_%{mod_name}.%{version}
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	top_dir=%{_pkglibdir} \
	APXS=%{apxs} \
	INCLUDES="-I%(%{apxs} -q INCLUDEDIR)"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/70_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc AUTHOR ChangeLog
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
