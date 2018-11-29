cmake_minimum_required(VERSION 3.12)
project(project)

set(CMAKE_CXX_STANDARD 14)

include_directories(src)
include_directories(wifi-sniffer-master)

add_executable(project
        src/sniff.cpp
        src/sniff.h
        wifi-sniffer-master/bin/cmake_install.cmake
        wifi-sniffer-master/bin/CMakeCache.txt
        wifi-sniffer-master/bin/Makefile
        wifi-sniffer-master/cmake/FindPCAP.cmake
        wifi-sniffer-master/cmake-build-debug/cmake_install.cmake
        wifi-sniffer-master/cmake-build-debug/CMakeCache.txt
        wifi-sniffer-master/cmake-build-debug/Makefile
        wifi-sniffer-master/cmake-build-debug/wifi-sniffer.cbp
        wifi-sniffer-master/CMakeLists.txt
        wifi-sniffer-master/LICENSE
        wifi-sniffer-master/main.cpp
        wifi-sniffer-master/protocol_headers.h
        wifi-sniffer-master/README.md
        wifi-sniffer-master/sniffer.cpp
        wifi-sniffer-master/sniffer.h
        wifi-sniffer-master/util.cpp
        wifi-sniffer-master/util.h)
