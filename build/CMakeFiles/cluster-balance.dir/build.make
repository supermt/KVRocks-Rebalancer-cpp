# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/build

# Include any dependencies generated for this target.
include CMakeFiles/cluster-balance.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/cluster-balance.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/cluster-balance.dir/flags.make

CMakeFiles/cluster-balance.dir/main.cpp.o: CMakeFiles/cluster-balance.dir/flags.make
CMakeFiles/cluster-balance.dir/main.cpp.o: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/cluster-balance.dir/main.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/cluster-balance.dir/main.cpp.o -c /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/main.cpp

CMakeFiles/cluster-balance.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/cluster-balance.dir/main.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/main.cpp > CMakeFiles/cluster-balance.dir/main.cpp.i

CMakeFiles/cluster-balance.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/cluster-balance.dir/main.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/main.cpp -o CMakeFiles/cluster-balance.dir/main.cpp.s

# Object files for target cluster-balance
cluster__balance_OBJECTS = \
"CMakeFiles/cluster-balance.dir/main.cpp.o"

# External object files for target cluster-balance
cluster__balance_EXTERNAL_OBJECTS =

cluster-balance: CMakeFiles/cluster-balance.dir/main.cpp.o
cluster-balance: CMakeFiles/cluster-balance.dir/build.make
cluster-balance: /usr/lib/x86_64-linux-gnu/libhiredis.so
cluster-balance: /usr/local/lib/libredis++.so
cluster-balance: CMakeFiles/cluster-balance.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable cluster-balance"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/cluster-balance.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/cluster-balance.dir/build: cluster-balance

.PHONY : CMakeFiles/cluster-balance.dir/build

CMakeFiles/cluster-balance.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/cluster-balance.dir/cmake_clean.cmake
.PHONY : CMakeFiles/cluster-balance.dir/clean

CMakeFiles/cluster-balance.dir/depend:
	cd /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/build /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/build /home/supermt/CLionProjects/KVRocks-Rebalancer-cpp/build/CMakeFiles/cluster-balance.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/cluster-balance.dir/depend
