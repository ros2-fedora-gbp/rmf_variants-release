%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-rmf-dev
Version:        0.0.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS rmf_dev package

License:        Apache License 2.0
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-rolling-ament-cmake-catch2
Requires:       ros-rolling-menge-vendor
Requires:       ros-rolling-nlohmann-json-schema-validator-vendor
Requires:       ros-rolling-pybind11-json-vendor
Requires:       ros-rolling-rmf-api-msgs
Requires:       ros-rolling-rmf-battery
Requires:       ros-rolling-rmf-building-map-msgs
Requires:       ros-rolling-rmf-building-map-tools
Requires:       ros-rolling-rmf-building-sim-common
Requires:       ros-rolling-rmf-building-sim-gz-classic-plugins
Requires:       ros-rolling-rmf-building-sim-gz-plugins
Requires:       ros-rolling-rmf-charger-msgs
Requires:       ros-rolling-rmf-dispenser-msgs
Requires:       ros-rolling-rmf-door-msgs
Requires:       ros-rolling-rmf-fleet-adapter
Requires:       ros-rolling-rmf-fleet-adapter-python
Requires:       ros-rolling-rmf-fleet-msgs
Requires:       ros-rolling-rmf-ingestor-msgs
Requires:       ros-rolling-rmf-lift-msgs
Requires:       ros-rolling-rmf-obstacle-msgs
Requires:       ros-rolling-rmf-robot-sim-common
Requires:       ros-rolling-rmf-robot-sim-gz-classic-plugins
Requires:       ros-rolling-rmf-robot-sim-gz-plugins
Requires:       ros-rolling-rmf-scheduler-msgs
Requires:       ros-rolling-rmf-site-map-msgs
Requires:       ros-rolling-rmf-task
Requires:       ros-rolling-rmf-task-msgs
Requires:       ros-rolling-rmf-task-ros2
Requires:       ros-rolling-rmf-task-sequence
Requires:       ros-rolling-rmf-traffic
Requires:       ros-rolling-rmf-traffic-editor
Requires:       ros-rolling-rmf-traffic-editor-assets
Requires:       ros-rolling-rmf-traffic-editor-test-maps
Requires:       ros-rolling-rmf-traffic-examples
Requires:       ros-rolling-rmf-traffic-msgs
Requires:       ros-rolling-rmf-traffic-ros2
Requires:       ros-rolling-rmf-utils
Requires:       ros-rolling-rmf-visualization
Requires:       ros-rolling-rmf-visualization-building-systems
Requires:       ros-rolling-rmf-visualization-fleet-states
Requires:       ros-rolling-rmf-visualization-floorplans
Requires:       ros-rolling-rmf-visualization-msgs
Requires:       ros-rolling-rmf-visualization-navgraphs
Requires:       ros-rolling-rmf-visualization-obstacles
Requires:       ros-rolling-rmf-visualization-rviz2-plugins
Requires:       ros-rolling-rmf-visualization-schedule
Requires:       ros-rolling-rmf-websocket
Requires:       ros-rolling-rmf-workcell-msgs
Requires:       ros-rolling-ros-workspace
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
A package to aggregate the packages required for a minimal installation of Open-
RMF

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Tue Jun 20 2023 Yadunund <yadunund@openrobotics.org> - 0.0.1-1
- Autogenerated by Bloom

