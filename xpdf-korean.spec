Summary:	ISO-2022-KR (KSX1001) encoding support for xpdf
Summary(pl.UTF-8):	Obsługa kodowania ISO-2022-KR (KSX1001) dla xpdf
Name:		xpdf-korean
Version:	20170725
Release:	1
License:	GPL v2 or GPL v3
Group:		X11/Applications
#Source0Download: http://www.xpdfreader.com/download.html
Source0:	https://xpdfreader-dl.s3.amazonaws.com/%{name}.tar.gz
# Source0-md5:	244d96e42ada05b9b96d999974a8dd5b
URL:		http://www.xpdfreader.com/
Requires(post,preun):	grep
Requires(post,preun):	xpdf
Requires(preun):	fileutils
Requires:	xpdf
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Xpdf language support packages include CMap files, text encodings,
and various other configuration information necessary or useful for
specific character sets. (They do not include any fonts.)
This package provides support files needed to use the Xpdf tools with
Korean PDF files.

%description -l pl.UTF-8
Pakiety wspierające języki Xpdf zawierają pliki CMap, kodowania oraz
różne inne informacje konfiguracyjne niezbędne bądź przydatne przy
określonych zestawach znaków (nie zawierają żadnych fontów).
Ten pakiet zawiera pliki potrzebne do używania narzędzi Xpdf z
koreańskimi plikami PDF.

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
	echo 'unicodeMap	ISO-2022-KR	/usr/share/xpdf/ISO-2022-KR.unicodeMap' >> /etc/xpdfrc
	echo 'cidToUnicode	Adobe-Korea1	/usr/share/xpdf/Adobe-Korea1.cidToUnicode' >> /etc/xpdfrc
	echo 'cMapDir		Adobe-Korea1	/usr/share/xpdf/CMap-korean' >> /etc/xpdfrc
	echo 'toUnicodeDir			/usr/share/xpdf/CMap-korean' >> /etc/xpdfrc
	echo 'displayCIDFontX	Adobe-Korea1	"-*-mincho-medium-r-normal-*-%s-*-*-*-*-*-ksc5601.1987-0" ISO-2022-KR' >> /etc/xpdfrc
else
 if ! grep -q 'ISO-2022-KR\.unicodeMap' /etc/xpdfrc; then
	echo 'unicodeMap	ISO-2022-KR	/usr/share/xpdf/ISO-2022-KR.unicodeMap' >> /etc/xpdfrc
 fi
 if ! grep -q 'Adobe-Korea1\.cidToUnicode' /etc/xpdfrc; then
	echo 'cidToUnicode	Adobe-Korea1	/usr/share/xpdf/Adobe-Korea1.cidToUnicode' >> /etc/xpdfrc
 fi
 if ! grep -q 'CMap-korean' /etc/xpdfrc; then
	echo 'cMapDir		Adobe-Korea1	/usr/share/xpdf/CMap-korean' >> /etc/xpdfrc
	echo 'toUnicodeDir			/usr/share/xpdf/CMap-korean' >> /etc/xpdfrc
 fi
 if ! grep -q -e '-\*-mincho-medium-r-normal-\*-%s-\*-\*-\*-\*-\*-ksc5601\.1987-0' /etc/xpdfrc; then
	echo 'displayCIDFontX	Adobe-Korea1	"-*-mincho-medium-r-normal-*-%s-*-*-*-*-*-ksc5601.1987-0" ISO-2022-KR' >> /etc/xpdfrc
 fi
fi

%preun
if [ "$1" = "0" ]; then
	umask 022
	grep -v 'ISO-2022-KR\.unicodeMap' /etc/xpdfrc > /etc/xpdfrc.new
	grep -v 'Adobe-Korea1\.cidToUnicode' /etc/xpdfrc.new > /etc/xpdfrc
	grep -v 'CMap-korean' /etc/xpdfrc > /etc/xpdfrc.new
	grep -v -e '-\*-mincho-medium-r-normal-\*-%s-\*-\*-\*-\*-\*-ksc5601\.1987-0' /etc/xpdfrc.new > /etc/xpdfrc
	rm -f /etc/xpdfrc.new
fi

%files
%defattr(644,root,root,755)
%doc README add-to-xpdfrc
%{_datadir}/xpdf/Adobe-Korea1.cidToUnicode
%{_datadir}/xpdf/ISO-2022-KR.unicodeMap
%{_datadir}/xpdf/CMap-korean
