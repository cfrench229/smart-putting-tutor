cmake_minimum_required(VERSION 3.15)

project(PuttingTutor LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Core library
add_library(putting_core
    src/imu.cpp
    src/logger.cpp
)

target_include_directories(putting_core
    PUBLIC
        ${PROJECT_SOURCE_DIR}/src
)

# Main executable
add_executable(putting_tutor
    src/main.cpp
)

target_link_libraries(putting_tutor
    PRIVATE putting_core
)

# Tests
enable_testing()

add_executable(tests
    tests/test_placeholder.cpp
)

target_link_libraries(tests
    PRIVATE putting_core
)

add_test(NAME ExampleTest COMMAND tests)
