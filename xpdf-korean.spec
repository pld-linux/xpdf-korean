Summary:	ISO-2022-KR (KSX1001) encoding support for xpdf
Summary(pl):	Wsparcie kodowania ISO-2022-KR (KSX1001) dla xpdf
Name:		xpdf-korean
Version:	1.0
Release:	3
License:	GPL
Group:		X11/Applications
Source0:	ftp://ftp.foolabs.com/pub/xpdf/%{name}.tar.gz
URL:		http://www.foolabs.com/xpdf/
Requires(post,preun):	grep
Requires(post,preun):	xpdf
Requires(preun):	fileutils
Requires:	xpdf
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
The Xpdf language support packages include CMap files, text encodings,
and various other configuration information necessary or useful for
specific character sets. (They do not include any fonts.) 
This package provides support files needed to use the Xpdf tools with
Korean PDF files.

%description -l pl
Pakiety wspieraj±ce jêzyki Xpdf zawieraj± pliki CMap, kodowania oraz
ró¿ne inne informacje konfiguracyjne niezbêdne b±d¼ przydatne przy
okre¶lonych zestawach znaków. (Nie zawieraj± ¿adnych fontów).
Ten pakiet zawiera pliki potrzebne do u¿ywania narzêdzi Xpdf z
koreañskimi plikami PDF.

%prep
%setup -q -n %{name}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/xpdf/CMap-korean

install *.unicodeMap $RPM_BUILD_ROOT%{_datadir}/xpdf
install *.cidToUnicode $RPM_BUILD_ROOT%{_datadir}/xpdf
install CMap/* $RPM_BUILD_ROOT%{_datadir}/xpdf/CMap-korean

%clean
rm -rf $RPM_BUILD_ROOT

%post
umask 022
if [ ! -f /etc/xpdfrc ]; then
	echo 'unicodeMap	ISO-2022-KR	/usr/X11R6/share/xpdf/ISO-2022-KR.unicodeMap' >> /etc/xpdfrc
	echo 'cidToUnicode	Adobe-Korea1	/usr/X11R6/share/xpdf/Adobe-Korea1.cidToUnicode' >> /etc/xpdfrc
	echo 'cMapDir		Adobe-Korea1	/usr/X11R6/share/xpdf/CMap-korean' >> /etc/xpdfrc
	echo 'toUnicodeDir			/usr/X11R6/share/xpdf/CMap-korean' >> /etc/xpdfrc
	echo 'displayCIDFontX	Adobe-Korea1	"-*-mincho-medium-r-normal-*-%s-*-*-*-*-*-ksc5601.1987-0" ISO-2022-KR' >> /etc/xpdfrc
else
 if ! grep -q 'ISO-2022-KR\.unicodeMap' /etc/xpdfrc; then
	echo 'unicodeMap	ISO-2022-KR	/usr/X11R6/share/xpdf/ISO-2022-KR.unicodeMap' >> /etc/xpdfrc
 fi
 if ! grep -q 'Adobe-Korea1\.cidToUnicode' /etc/xpdfrc; then
	echo 'cidToUnicode	Adobe-Korea1	/usr/X11R6/share/xpdf/Adobe-Korea1.cidToUnicode' >> /etc/xpdfrc
 fi
 if ! grep -q 'CMap-korean' /etc/xpdfrc; then
	echo 'cMapDir		Adobe-Korea1	/usr/X11R6/share/xpdf/CMap-korean' >> /etc/xpdfrc
	echo 'toUnicodeDir			/usr/X11R6/share/xpdf/CMap-korean' >> /etc/xpdfrc
 fi
 if ! grep -q -e '-\*-mincho-medium-r-normal-\*-%s-\*-\*-\*-\*-\*-ksc5601\.1987-0' /etc/xpdfrc; then
	echo 'displayCIDFontX	Adobe-Korea1	"-*-mincho-medium-r-normal-*-%s-*-*-*-*-*-ksc5601.1987-0" ISO-2022-KR' >> /etc/xpdfrc
 fi
fi

%preun
umask 022
grep -v 'ISO-2022-KR\.unicodeMap' /etc/xpdfrc > /etc/xpdfrc.new
grep -v 'Adobe-Korea1\.cidToUnicode' /etc/xpdfrc.new > /etc/xpdfrc
grep -v 'CMap-korean' /etc/xpdfrc > /etc/xpdfrc.new
grep -v -e '-\*-mincho-medium-r-normal-\*-%s-\*-\*-\*-\*-\*-ksc5601\.1987-0' /etc/xpdfrc.new > /etc/xpdfrc
rm -f /etc/xpdfrc.new

%files
%defattr(644,root,root,755)
%doc README add-to-xpdfrc
%{_datadir}/xpdf/*
