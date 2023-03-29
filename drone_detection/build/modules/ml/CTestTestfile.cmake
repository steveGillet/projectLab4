# CMake generated Testfile for 
# Source directory: /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/ml
# Build directory: /home/rishi/projectLab4/drone_detection/build/modules/ml
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(opencv_test_ml "/home/rishi/projectLab4/drone_detection/build/bin/opencv_test_ml" "--gtest_output=xml:opencv_test_ml.xml")
set_tests_properties(opencv_test_ml PROPERTIES  LABELS "Main;opencv_ml;Accuracy" WORKING_DIRECTORY "/home/rishi/projectLab4/drone_detection/build/test-reports/accuracy" _BACKTRACE_TRIPLES "/home/rishi/projectLab4/drone_detection/opencv-4.x/cmake/OpenCVUtils.cmake;1763;add_test;/home/rishi/projectLab4/drone_detection/opencv-4.x/cmake/OpenCVModule.cmake;1375;ocv_add_test_from_target;/home/rishi/projectLab4/drone_detection/opencv-4.x/cmake/OpenCVModule.cmake;1133;ocv_add_accuracy_tests;/home/rishi/projectLab4/drone_detection/opencv-4.x/modules/ml/CMakeLists.txt;2;ocv_define_module;/home/rishi/projectLab4/drone_detection/opencv-4.x/modules/ml/CMakeLists.txt;0;")
