# TODO: find fits.jar, netcdf.jar, slf4j-api, slf4j-nop source, build separately
Summary:	HDF Java Products
Summary(pl.UTF-8):	Produkty HDF Java
Name:		hdf-java
Version:	2.11.0
Release:	2
Group:		Applications/File
License:	BSD-like, changed sources must be marked
Source0:	https://support.hdfgroup.org/ftp/HDF5/releases/HDF-JAVA/hdf-java-2.11/src/%{name}-%{version}.tar.gz
# Source0-md5:	22c071948d9d140506e0f91fa1855f27
Patch0:		%{name}-configure.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-hdfview.patch
URL:		http://portal.hdfgroup.org/display/support/HDF-Java
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	h4h5tools-devel
BuildRequires:	hdf-devel >= 4
BuildRequires:	hdf5-devel
BuildRequires:	szip-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The HDF Java Products include HDFView, Java HDF Object Package, and
Java HDF4 and HDF5 Interfaces.

%description -l pl.UTF-8
Produkty HDF Java obejmują HDFView, pakiet Java HDF Object oraz
interfejsy Javy HDF4 i HDF5.

%package -n java-hdf
Summary:	Java HDF Interface (JHI)
Summary(pl.UTF-8):	Interfejs HDF do Javy (JHI)
Group:		Libraries/Java
URL:		http://www.hdfgroup.org/hdf-java-html/JNI/jhi/index.html
Requires:	java-slf4j >= 1.7.5

%description -n java-hdf
The Java Native Interface to the standard HDF4 library.

%description -n java-hdf -l pl.UTF-8
Natywny interfejs Javy (JNI) do biblioteki standardowej HDF4.

%package -n java-hdf5
Summary:	Java HDF5 Interface (JHI5)
Summary(pl.UTF-8):	Interfejs HDF5 do Javy (JHI5)
Group:		Libraries/Java
URL:		http://www.hdfgroup.org/hdf-java-html/JNI/jhi5/index.html
Requires:	java-slf4j >= 1.7.5

%description -n java-hdf5
The Java Native Interface to the standard HDF5 library.

%description -n java-hdf5 -l pl.UTF-8
Natywny interfejs Javy (JNI) do biblioteki standardowej HDF5.

%package -n java-hdf-object
Summary:	Java HDF Object Package
Summary(pl.UTF-8):	Pakiet Javy HDF Object
Group:		Libraries/Java
URL:		http://www.hdfgroup.org/hdf-java-html/hdf-object/index.html
Requires:	java-hdf = %{version}-%{release}
Requires:	java-hdf5 = %{version}-%{release}

%description -n java-hdf-object
Java package that implements HDF4 and HDF5 data objects in an
object-oriented form.

%description -n java-hdf-object -l pl.UTF-8
Pakiet Javy z implementacją obiektów danych HDF w postaci
zorientowanej obiektowo.

%package -n hdfview
Summary:	HDFView - visual tool for browsing and editing HDF4 and HDF5 files
Summary(pl.UTF-8):	HDFView - graficzne narzędzie do przeglądania i edycji plików HDF4 i HDF5
Group:		Applications/File
URL:		http://www.hdfgroup.org/hdf-java-html/hdfview/index.html
Requires:	java-hdf-object = %{version}-%{release}

%description -n hdfview
HDFView is a visual tool for browsing and editing HDF4 and HDF5 files.
Using HDFView, you can:
 - view a file hierarchy in a tree structure
 - create new file, add or delete groups and datasets
 - view and modify the content of a dataset
 - add, delete and modify attributes
 - replace I/O and GUI components such as table view, image view and
   metadata view

%description -n hdfview -l pl.UTF-8
HDFView to graficzne narzędzie do przeglądania i edycji plików HDF4 i
HDF5. Przy jego użyciu można:
 - oglądać hierarchię pliku w strukturze drzewiastej
 - utworzyć nowy plik, dodawać i usuwać grupy i zbiory danych
 - oglądać i modyfikować zawartość zbioru danych
 - dodawać, usuwać i modyfikować atrybuty
 - podmieniać komponenty we/wy i GUI, takie jak widok tabeli, widok
   obrazu czy widok metadanych.

%package javadoc
Summary:	Javadoc documentation for hdf-java classes
Summary(pl.UTF-8):	Dokumentacja javadoc dla klas hdf-java
Group:		Documentation

%description javadoc
Javadoc documentation for hdf-java classes.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla klas hdf-java.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.* config
%{__autoconf}
%configure \
	--with-h4toh5 \
	--with-hdf4=%{_includedir}/hdf,%{_libdir} \
	--with-hdf5=%{_includedir},%{_libdir} \
	--with-jdk=%{_jvmdir}/java/include,%{_jvmdir}/java/jre/lib \
	--with-libjpeg \
	--with-libsz \
	--with-libz

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	JARDIR=$RPM_BUILD_ROOT%{_javadir} \
	DOCDIR=$RPM_BUILD_ROOT%{_docdir}

# in java-junit
%{__rm} $RPM_BUILD_ROOT%{_javadir}/junit.jar
# in java-slf4j
%{__rm} $RPM_BUILD_ROOT%{_javadir}/slf4j-*.jar

install -d $RPM_BUILD_ROOT%{_javadocdir}
cp -pr docs/javadocs $RPM_BUILD_ROOT%{_javadocdir}/hdf-java

%clean
rm -rf $RPM_BUILD_ROOT

%files -n java-hdf
%defattr(644,root,root,755)
%doc COPYING Readme.txt
%attr(755,root,root) %{_libdir}/libjhdf.so
%{_javadir}/jhdf.jar

%files -n java-hdf5
%defattr(644,root,root,755)
%doc COPYING Readme.txt
%attr(755,root,root) %{_libdir}/libjhdf5.so
%{_javadir}/jhdf5.jar

%files -n java-hdf-object
%defattr(644,root,root,755)
%{_javadir}/fitsobj.jar
%{_javadir}/jhdfobj.jar
%{_javadir}/jhdf4obj.jar
%{_javadir}/jhdf5obj.jar
%{_javadir}/nc2obj.jar
# NOTE: external jars
%{_javadir}/fits.jar
%{_javadir}/netcdf.jar

%files -n hdfview
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/hdfview.sh
%{_javadir}/jhdfview.jar

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/hdf-java
