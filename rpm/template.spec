Name:           ros-indigo-rocon-python-hue
Version:        0.0.6
Release:        0%{?dist}
Summary:        ROS rocon_python_hue package

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/studioimaginaire/phue
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  ros-indigo-catkin

%description
The patched version of phue(r7) wrapper - Create the exception.py and move the
exception class - Add the &quot;reachable&quot; flag. Possible to get the each
bulb validation. - Connection method change. No more use the user name. The user
name is pre-define to &quot;newdeveloper&quot;. It has the all permission of hue
restapi.

%prep
%setup -q

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
mkdir -p obj-%{_target_platform} && cd obj-%{_target_platform}
%cmake .. \
        -UINCLUDE_INSTALL_DIR \
        -ULIB_INSTALL_DIR \
        -USYSCONF_INSTALL_DIR \
        -USHARE_INSTALL_PREFIX \
        -ULIB_SUFFIX \
        -DCMAKE_INSTALL_PREFIX="/opt/ros/indigo" \
        -DCMAKE_PREFIX_PATH="/opt/ros/indigo" \
        -DSETUPTOOLS_DEB_LAYOUT=OFF \
        -DCATKIN_BUILD_BINARY_PACKAGE="1" \

make %{?_smp_mflags}

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree that was dropped by catkin, and source it.  It will
# set things like CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/indigo/setup.sh" ]; then . "/opt/ros/indigo/setup.sh"; fi
cd obj-%{_target_platform}
make %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
/opt/ros/indigo

%changelog
* Thu Jul 23 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.6-0
- Autogenerated by Bloom

* Thu Jul 09 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.5-0
- Autogenerated by Bloom

* Mon Jun 15 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.4-0
- Autogenerated by Bloom

* Fri Jun 05 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.3-0
- Autogenerated by Bloom

* Fri Jun 05 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.2-0
- Autogenerated by Bloom

* Tue Jun 02 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.1-0
- Autogenerated by Bloom
