cmake_minimum_required(VERSION 3.16)
project(PuttingTutor)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Option to build with samples
option(BUILD_WITH_SAMPLES "Build with sample strokes for testing" OFF)

# Source files
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

# Add executable
add_executable(putting_tutor ${SOURCES})

# Modern include directories (only for this target)
target_include_directories(putting_tutor PRIVATE include)

# Output binary to bin/
set_target_properties(putting_tutor PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin
)
