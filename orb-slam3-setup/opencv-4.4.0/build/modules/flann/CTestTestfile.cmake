# CMake generated Testfile for 
# Source directory: /home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/modules/flann
# Build directory: /home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/build/modules/flann
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_flann "/home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/build/bin/opencv_test_flann" "--gtest_output=xml:opencv_test_flann.xml")
set_tests_properties(opencv_test_flann PROPERTIES  LABELS "Main;opencv_flann;Accuracy" WORKING_DIRECTORY "/home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/cmake/OpenCVUtils.cmake;1640;add_test;/home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/cmake/OpenCVModule.cmake;1310;ocv_add_test_from_target;/home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/cmake/OpenCVModule.cmake;1074;ocv_add_accuracy_tests;/home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/modules/flann/CMakeLists.txt;2;ocv_define_module;/home/cai/Dev/rc_smart_cart/orb-slam3-setup/opencv-4.4.0/modules/flann/CMakeLists.txt;0;")
