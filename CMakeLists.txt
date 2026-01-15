cmake_minimum_required(VERSION 3.16)
project(PuttingTutor)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# -------------------------
# Options
# -------------------------
option(BUILD_WITH_SAMPLES "Build with sample strokes for testing" OFF)
option(BUILD_TESTS "Build unit tests" OFF)
option(BUILD_FOR_ARM "Build for ARM target (Pi Zero 2 W)" OFF)

# -------------------------
# ARM detection / flags
# -------------------------
if(BUILD_FOR_ARM)
    message(STATUS "Building for ARM target")
    add_definitions(-DARM_BUILD)
    # Optional: additional flags
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2 -march=armv8-a")
endif()

# -------------------------
# Main application sources
# -------------------------
set(SOURCES
    src/main.cpp
    src/core/stroke_features.cpp
)

# Conditionally add sample loader
if(BUILD_WITH_SAMPLES)
    message(STATUS "Building with sample strokes")
    add_definitions(-DUSE_SAMPLES)
    list(APPEND SOURCES src/sample_loader.cpp)
endif()

# Main executable
add_executable(putting_tutor ${SOURCES})
target_include_directories(putting_tutor PRIVATE include)


# Use the CMAKE_RUNTIME_OUTPUT_DIRECTORY if defined; otherwise default to PROJECT_SOURCE_DIR/bin
if(NOT DEFINED CMAKE_RUNTIME_OUTPUT_DIRECTORY)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
endif()

set_target_properties(putting_tutor PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}
)


# -------------------------
# Unit tests
# -------------------------
if(BUILD_TESTS)
    message(STATUS "Building unit tests")

    include(FetchContent)

    FetchContent_Declare(
        googletest
        URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.zip
        DOWNLOAD_EXTRACT_TIMESTAMP TRUE
    )

    set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
    FetchContent_MakeAvailable(googletest)

    enable_testing()

    add_executable(stroke_tests
        tests/test_stroke_features.cpp
        src/core/stroke_features.cpp
    )

    target_include_directories(stroke_tests PRIVATE include)

    target_link_libraries(stroke_tests
        GTest::gtest_main
    )

    include(GoogleTest)
    gtest_discover_tests(stroke_tests)
endif()
