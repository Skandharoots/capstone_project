cmake_minimum_required(VERSION 3.16...3.26)
project(kiss_icp_pybind VERSION 0.3.0 LANGUAGES CXX)

# Set build type
set(CMAKE_BUILD_TYPE Release)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

set(PYBIND11_NEWPYTHON ON)
find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)

set(KISS_ICP_SOURCE_PATH "E:/capstonecode/src/cpp/kiss_icp")

add_subdirectory(${KISS_ICP_SOURCE_PATH} ${CMAKE_CURRENT_BINARY_DIR}/kiss_icp)
add_subdirectory(kiss_icp/pybind)
