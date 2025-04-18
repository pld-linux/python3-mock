#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

%define		module	mock
Summary:	Rolling backport of unittest.mock for all Pythons
Summary(pl.UTF-8):	Podążający backport modułu unittest.mock dla wszystkich wersji Pythona
Name:		python3-%{module}
Version:	5.2.0
Release:	1
License:	BSD
Group:		Development/Languages/Python
##Source0Download: https://pypi.org/simple/mock/
#Source0:	https://files.pythonhosted.org/packages/source/m/mock/%{module}-%{version}.tar.gz
# pypi dist misses docs and tests, use github archive
#Source0Download: https://github.com/testing-cabal/mock/releases
Source0:	https://github.com/testing-cabal/mock/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	ee1baedbfa514889dce013e6b0dba8b8
URL:		http://python-mock.sourceforge.net/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:17.1
%if %{with tests}
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
mock is a library for testing in Python. It allows you to replace
parts of your system under test with mock objects and make assertions
about how they have been used.

mock provides a core `MagicMock` class removing the need to create a
host of stubs throughout your test suite. After performing an action,
you can make assertions about which methods/attributes were used and
arguments they were called with. You can also specify return values
and set needed attributes in the normal way.

The mock module also provides utility functions/objects to assist with
testing, particularly monkey patching.

%description -l pl.UTF-8
mock to biblioteka do testowania w Pythonie. Pozwala na zastępowanie
części testowanego systemu obiektami "mock" oraz sprawdzania zapewnień
(assert) o tym, jak zostały użyte.

mock udostępnia klasę główną "MagicMock", dzięki której nie trzeba
tworzyć systemu zaślepek do testów. W czasie wykonywania akcji można
kontrolować, czy odpowiednie metody/atrybuty zostały użyte i z jakimi
argumentami. Można określić zwracane wartości i w zwykły sposób
ustawiać potrzebne atrybuty.

Moduł mock udostępnia także funkcje/obiekty narzędziowe pomagające
przy testowaniu, w szczególności łataniu.

%package apidocs
Summary:	API documentation for mock module
Summary(pl.UTF-8):	Dokumentacja API modułu mock
Group:		Documentation

%description apidocs
API documentation for mock module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu mock.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build

%if %{with tests}
# disable plugins (e.g. pytest-mock) to avoid changing assert output
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest mock/tests
%endif

%if %{with doc}
PYTHONPATH=. sphinx-build-3 -b html docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGELOG.rst LICENSE.txt README.rst
%{py3_sitescriptdir}/mock
%{py3_sitescriptdir}/%{module}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc html/{_static,*.html,*.js}
%endif
