Name:           ros-indigo-rocon-ninjablock-bridge
Version:        0.0.7
Release:        0%{?dist}
Summary:        ROS rocon_ninjablock_bridge package

Group:          Development/Libraries
License:        BSD
URL:            http://wiki.ros.org/rocon_ninjablock_bridge
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-indigo-rocon-device-msgs
Requires:       ros-indigo-rocon-iot-bridge
Requires:       ros-indigo-rocon-std-msgs
Requires:       ros-indigo-rospy
BuildRequires:  ros-indigo-catkin
BuildRequires:  ros-indigo-rocon-iot-bridge
BuildRequires:  ros-indigo-rospy

%description
bridging the ninjablock devices and ROS

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
* Tue Jul 28 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.7-0
- Autogenerated by Bloom

* Thu Jul 23 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.6-0
- Autogenerated by Bloom

* Thu Jul 09 2015 Dongwook Lee <dwlee@yujinrobot.com> - 0.0.5-0
- Autogenerated by Bloom

