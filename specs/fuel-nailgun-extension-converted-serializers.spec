Name:           fuel-nailgun-extension-converted-serializers
Version:        9.0.1
Release:        1%{?dist}
Summary:        Converted serializers extension for Fuel
License:        Apache-2.0
Url:            https://git.openstack.org/cgit/openstack/fuel-nailgun-extension-converted-serializers/
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools

Requires:       fuel-nailgun
Requires:       python-pbr

%description
Converted serializers extension for Fuel

%prep
%setup -q -c -n %{name}-%{version}

%build
export OSLO_PACKAGE_VERSION=%{version}
%py2_build

%install
export OSLO_PACKAGE_VERSION=%{version}
%py2_install

%files
%license LICENSE
%{python2_sitelib}/converted_serializers
%{python2_sitelib}/*.egg-info

%changelog
* Thu Nov 29 2016 Roman Sokolkov <rsokolkov@mirantis.com> - 9.0.1-1
- Fix version for stable/mitaka (Downgrade).

* Thu Sep 8 2016 Vladimir Kuklin <vkuklin@mirantis.com> - 10.0~b1-1
- Initial package.
