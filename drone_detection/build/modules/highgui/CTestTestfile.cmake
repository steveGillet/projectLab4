# CMake generated Testfile for 
# Source directory: /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/highgui
# Build directory: /home/rishi/projectLab4/drone_detection/build/modules/highgui
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_highgui "/home/rishi/projectLab4/drone_detection/build/bin/opencv_test_highgui" "--gtest_output=xml:opencv_test_highgui.xml")
set_tests_properties(opencv_test_highgui PROPERTIES  LABELS "Main;opencv_highgui;Accuracy" WORKING_DIRECTORY "/home/rishi/projectLab4/drone_detection/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/rishi/projectLab4/drone_detection/opencv-4.x/cmake/OpenCVUtils.cmake;1763;add_test;/home/rishi/projectLab4/drone_detection/opencv-4.x/cmake/OpenCVModule.cmake;1375;ocv_add_test_from_target;/home/rishi/projectLab4/drone_detection/opencv-4.x/modules/highgui/CMakeLists.txt;309;ocv_add_accuracy_tests;/home/rishi/projectLab4/drone_detection/opencv-4.x/modules/highgui/CMakeLists.txt;0;")
