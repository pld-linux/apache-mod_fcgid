%define 	apxs	/usr/sbin/apxs
%define		_apache1        %(rpm -q apache-devel 2> /dev/null | grep -Eq '\\-2\\.[0-9]+\\.' && echo 0 || echo 1)
Summary:	A binary compatibility alternative to Apache module mod_fastcgi
Summary(pl):	Binarnie kompatybilna alternatywa dla modu³u Apache'a mod_fastcgi
Name:		apache-mod_fcgid
Version:	0.74
Release:	1
License:	distributable
Group:		Networking/Daemons
Source0:	http://fastcgi.coremail.cn/mod_fcgid.%{version}.tar.gz
# Source0-md5:	50c625f238c82cba3ed232cec3d3ca95
Source1:	70_mod_fcgid.conf
URL:		http://fastcgi.coremail.cn/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
Requires(post,preun):	%{apxs}
Requires:	apache >= 1.3.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _libexecdir     %{_libdir}/apache

%description
A binary compatibility alternative to Apache module mod_fastcgi.
mod_fcgid has a new process management strategy, which concentrates on
reducing the number of fastcgi server, and kick out the corrupt
fastcgi server as soon as possible.

%description -l pl
Binarnie kompatybilna alternatywa dla modu³u Apache'a mod_fastcgi.
mod_fcgid to nowa strategia zarz±dzania procesami, koncentruj±ca siê
na redukcji liczby serwerów fastcgi i usuwaniu uszkodzonych serwerów
fastcgi najszybciej jak to mo¿liwe.

%prep
%setup -q -n mod_fcgid.%{version}

%build
sed -i -e 's#top_dir.*=.*#top_dir = %{_libexecdir}#g' Makefile
echo "INCLUDES=`apr-config --includes` `apu-config --includes` -I%{_includedir}/apache" >> Makefile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libexecdir},%{_htmldocdir}}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/httpd/httpd.conf

libtool --mode=install install mod_fcgid.la $RPM_BUILD_ROOT%{_libexecdir}
install %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/httpd/httpd.conf/70_mod_fcgid.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/httpd ]; then
        /etc/rc.d/init.d/httpd restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/httpd start\" to start apache http daemon."
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
%attr(755,root,root) %{_libexecdir}/*.so
