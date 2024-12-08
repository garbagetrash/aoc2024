cmake_minimum_required(VERSION 3.20)
project(aoc2024)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_compile_definitions(-Dbase_dir="${CMAKE_CURRENT_SOURCE_DIR}")

include(FetchContent)

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY git@github.com:pybind/pybind11.git
)
FetchContent_MakeAvailable(pybind11)

add_executable(06 src/06.cpp)
target_include_directories(06 PRIVATE include)
