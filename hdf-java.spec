# NOTE: this package is obsolete; it uses 32-bit object identifiers.
# For hdf 4.2.12+ and hdf5 1.10+ use wrappers built from hdf.spec/hdf5.spec instead.
Summary:	HDF Java Products
Summary(pl.UTF-8):	Produkty HDF Java
Name:		hdf-java
Version:	3.3.2
Release:	0.1
Group:		Applications/File
License:	BSD-like, changed sources must be marked
Source0:	https://support.hdfgroup.org/ftp/HDF5/releases/HDF-JAVA/hdfjni-%{version}/src/HDFJava-%{version}-Source.tar.gz
# Source0-md5:	5d234a4ff22a010d4f140fa60be86e34
Patch0:		%{name}-configure.patch
Patch1:		%{name}-install.patch
Patch2:		%{name}-version.patch
URL:		http://portal.hdfgroup.org/display/support/HDF-Java
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	hdf-devel >= 4
BuildRequires:	hdf5-devel >= 1.8
BuildRequires:	hdf5-devel < 1.10
BuildRequires:	jdk
BuildRequires:	rpmbuild(macros) >= 1.294
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
URL:		http://portal.hdfgroup.org/display/HDFVIEW/JHI+Design+Notes
Requires:	java-slf4j >= 1.7.5

%description -n java-hdf
The Java Native Interface to the standard HDF4 library.

%description -n java-hdf -l pl.UTF-8
Natywny interfejs Javy (JNI) do biblioteki standardowej HDF4.

%package -n java-hdf5
Summary:	Java HDF5 Interface (JHI5)
Summary(pl.UTF-8):	Interfejs HDF5 do Javy (JHI5)
Group:		Libraries/Java
URL:		http://portal.hdfgroup.org/display/HDFVIEW/JHI5+Design+Notes
Requires:	java-slf4j >= 1.7.5

%description -n java-hdf5
The Java Native Interface to the standard HDF5 library.

%description -n java-hdf5 -l pl.UTF-8
Natywny interfejs Javy (JNI) do biblioteki standardowej HDF5.

%package javadoc
Summary:	Javadoc documentation for hdf-java classes
Summary(pl.UTF-8):	Dokumentacja javadoc dla klas hdf-java
Group:		Documentation

%description javadoc
Javadoc documentation for hdf-java classes.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla klas hdf-java.

%prep
%setup -q -n hdfjava-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
cp -f /usr/share/automake/config.* config
%{__autoconf}
CPPFLAGS="%{rpmcppflags} -DH5_USE_18_API"
%configure \
	--with-hdf4=%{_includedir}/hdf,%{_libdir} \
	--with-hdf5=%{_includedir},%{_libdir} \
	--with-jdk=%{_jvmdir}/java/include,%{_jvmdir}/java/jre/lib \
	--with-libjpeg \
	--with-libsz \
	--with-libz

%{__make}

install -d javadoc/{hdflib,hdf5lib}
TOPDIR=$(pwd)
cd hdf/hdflib
%javadoc -d "${TOPDIR}/javadoc/hdflib" \
	-author \
	-classpath lib/slf4j-api-1.7.5.tar \
	-doctitle "<h1>HDF Java Wrapper</h1>" \
	-use \
	-version \
	-windowtitle "HDF Java" \
	*.java

cd ../hdf5lib
%javadoc -d "${TOPDIR}/javadoc/hdf5lib" \
	-author \
	-classpath lib/slf4j-api-1.7.5.tar \
	-doctitle "<h1>HDF5 Java Wrapper</h1>" \
	-use \
	-version \
	-windowtitle "HDF5 Java" \
	callbacks/*.java \
	exceptions/*.java \
	structs/*.java \
	*.java

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	LIBDIR=$RPM_BUILD_ROOT%{_libdir} \
	JARDIR=$RPM_BUILD_ROOT%{_javadir} \
	DOCDIR=$RPM_BUILD_ROOT%{_docdir}

install -d $RPM_BUILD_ROOT%{_javadocdir}
cp -pr javadoc/{hdflib,hdf5lib} $RPM_BUILD_ROOT%{_javadocdir}

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

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/hdflib
%{_javadocdir}/hdf5lib
