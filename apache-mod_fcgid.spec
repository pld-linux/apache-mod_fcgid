%define		mod_name	fcgid
%define 	apxs		/usr/sbin/apxs
Summary:	A binary compatibility alternative to Apache module mod_fastcgi
Summary(pl):	Binarnie kompatybilna alternatywa dla modu³u Apache'a mod_fastcgi
Name:		apache-mod_%{mod_name}
Version:	1.03
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://fastcgi.coremail.cn/mod_%{mod_name}.%{version}.tar.gz
# Source0-md5:	dbcd5c96f8d6c6fcb7471abf527d176f
Source1:	%{name}.conf
Patch0:		%{name}-apr-status-is-success.patch
URL:		http://fastcgi.coremail.cn/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
Requires(post,preun):	%{apxs}
Requires:	apache >= 2.0.52-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR)
%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
A binary compatibility alternative to Apache module mod_fastcgi.
mod_fcgid has a new process management strategy, which concentrates
on reducing the number of fastcgi server, and kick out the corrupt
fastcgi server as soon as possible.

%description -l pl
Binarnie kompatybilna alternatywa dla modu³u Apache'a mod_fastcgi.
mod_fcgid to nowa strategia zarz±dzania procesami, koncentruj±ca siê
na redukcji liczby serwerów fastcgi i usuwaniu uszkodzonych serwerów
fastcgi najszybciej jak to mo¿liwe.

%prep
%setup -q -n mod_%{mod_name}.%{version}
%patch0 -p1

%build
%{__make} \
	top_dir=%{_pkglibdir} \
	APXS=%{_apxs} \
	INCLUDES="-I%(%{apxs} -q INCLUDEDIR)"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/httpd.conf}

install .libs/mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}
install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd.conf/70_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache HTTP daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc AUTHOR ChangeLog
%config(noreplace) /etc/httpd/httpd.conf/70_mod_fcgid.conf
%attr(755,root,root) %{_pkglibdir}/*.so
