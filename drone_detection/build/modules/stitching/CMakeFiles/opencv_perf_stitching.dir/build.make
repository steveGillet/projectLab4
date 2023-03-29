# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.26

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/local/bin/cmake

# The command to remove a file.
RM = /usr/local/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/rishi/projectLab4/drone_detection/opencv-4.x

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/rishi/projectLab4/drone_detection/build

# Include any dependencies generated for this target.
include modules/stitching/CMakeFiles/opencv_perf_stitching.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include modules/stitching/CMakeFiles/opencv_perf_stitching.dir/compiler_depend.make

# Include the progress variables for this target.
include modules/stitching/CMakeFiles/opencv_perf_stitching.dir/progress.make

# Include the compile flags for this target's objects.
include modules/stitching/CMakeFiles/opencv_perf_stitching.dir/flags.make

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/flags.make
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o: /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/opencl/perf_stitch.cpp
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rishi/projectLab4/drone_detection/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o -MF CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o.d -o CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o -c /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/opencl/perf_stitch.cpp

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.i"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/opencl/perf_stitch.cpp > CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.i

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.s"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/opencl/perf_stitch.cpp -o CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.s

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/flags.make
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o: /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/opencl/perf_warpers.cpp
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rishi/projectLab4/drone_detection/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o -MF CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o.d -o CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o -c /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/opencl/perf_warpers.cpp

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.i"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/opencl/perf_warpers.cpp > CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.i

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.s"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/opencl/perf_warpers.cpp -o CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.s

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/flags.make
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o: /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_estimators.cpp
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rishi/projectLab4/drone_detection/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o -MF CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o.d -o CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o -c /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_estimators.cpp

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.i"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_estimators.cpp > CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.i

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.s"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_estimators.cpp -o CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.s

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/flags.make
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o: /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_main.cpp
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rishi/projectLab4/drone_detection/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o -MF CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o.d -o CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o -c /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_main.cpp

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.i"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_main.cpp > CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.i

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.s"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_main.cpp -o CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.s

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/flags.make
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o: /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_matchers.cpp
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rishi/projectLab4/drone_detection/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o -MF CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o.d -o CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o -c /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_matchers.cpp

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.i"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_matchers.cpp > CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.i

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.s"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_matchers.cpp -o CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.s

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/flags.make
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o: /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_stich.cpp
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/rishi/projectLab4/drone_detection/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building CXX object modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o -MF CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o.d -o CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o -c /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_stich.cpp

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.i"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_stich.cpp > CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.i

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.s"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && /usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching/perf/perf_stich.cpp -o CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.s

# Object files for target opencv_perf_stitching
opencv_perf_stitching_OBJECTS = \
"CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o" \
"CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o" \
"CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o" \
"CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o" \
"CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o" \
"CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o"

# External object files for target opencv_perf_stitching
opencv_perf_stitching_EXTERNAL_OBJECTS =

bin/opencv_perf_stitching: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_stitch.cpp.o
bin/opencv_perf_stitching: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/opencl/perf_warpers.cpp.o
bin/opencv_perf_stitching: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_estimators.cpp.o
bin/opencv_perf_stitching: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_main.cpp.o
bin/opencv_perf_stitching: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_matchers.cpp.o
bin/opencv_perf_stitching: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/perf/perf_stich.cpp.o
bin/opencv_perf_stitching: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/build.make
bin/opencv_perf_stitching: lib/libopencv_ts.a
bin/opencv_perf_stitching: lib/libopencv_stitching.so.4.7.0
bin/opencv_perf_stitching: lib/libopencv_highgui.so.4.7.0
bin/opencv_perf_stitching: lib/libopencv_calib3d.so.4.7.0
bin/opencv_perf_stitching: lib/libopencv_videoio.so.4.7.0
bin/opencv_perf_stitching: lib/libopencv_imgcodecs.so.4.7.0
bin/opencv_perf_stitching: 3rdparty/lib/libtegra_hal.a
bin/opencv_perf_stitching: lib/libopencv_features2d.so.4.7.0
bin/opencv_perf_stitching: lib/libopencv_flann.so.4.7.0
bin/opencv_perf_stitching: lib/libopencv_imgproc.so.4.7.0
bin/opencv_perf_stitching: lib/libopencv_core.so.4.7.0
bin/opencv_perf_stitching: modules/stitching/CMakeFiles/opencv_perf_stitching.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/rishi/projectLab4/drone_detection/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Linking CXX executable ../../bin/opencv_perf_stitching"
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/opencv_perf_stitching.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
modules/stitching/CMakeFiles/opencv_perf_stitching.dir/build: bin/opencv_perf_stitching
.PHONY : modules/stitching/CMakeFiles/opencv_perf_stitching.dir/build

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/clean:
	cd /home/rishi/projectLab4/drone_detection/build/modules/stitching && $(CMAKE_COMMAND) -P CMakeFiles/opencv_perf_stitching.dir/cmake_clean.cmake
.PHONY : modules/stitching/CMakeFiles/opencv_perf_stitching.dir/clean

modules/stitching/CMakeFiles/opencv_perf_stitching.dir/depend:
	cd /home/rishi/projectLab4/drone_detection/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/rishi/projectLab4/drone_detection/opencv-4.x /home/rishi/projectLab4/drone_detection/opencv-4.x/modules/stitching /home/rishi/projectLab4/drone_detection/build /home/rishi/projectLab4/drone_detection/build/modules/stitching /home/rishi/projectLab4/drone_detection/build/modules/stitching/CMakeFiles/opencv_perf_stitching.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : modules/stitching/CMakeFiles/opencv_perf_stitching.dir/depend

