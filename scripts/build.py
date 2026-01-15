#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

# ----------- Configuration -----------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")
JSON_REPO = "https://github.com/nlohmann/json.git"
JSON_INCLUDE_DIR = os.path.join(PROJECT_ROOT, "include", "nlohmann")
JSON_HEADER = os.path.join(JSON_INCLUDE_DIR, "json.hpp")
TEMP_REPO_DIR = os.path.join(PROJECT_ROOT, "tmp_json_repo")

# Build folders
BUILD_DIR_X86 = os.path.join(PROJECT_ROOT, "build-x86")
BUILD_DIR_ARM = os.path.join(PROJECT_ROOT, "build-arm64")
BUILD_DIR_TESTS = os.path.join(PROJECT_ROOT, "build-tests")

TOOLCHAIN_FILE = os.path.join(PROJECT_ROOT, "toolchain-arm64.cmake")

# ----------- Helper functions -----------

def run_setup():
    """Clone nlohmann/json and place json.hpp in include folder."""
    os.makedirs(JSON_INCLUDE_DIR, exist_ok=True)

    if os.path.exists(JSON_HEADER):
        print("json.hpp already exists, skipping download.")
        return

    print(f"Cloning nlohmann/json into temporary folder {TEMP_REPO_DIR}...")
    subprocess.run([
        "git", "clone", "--depth", "1", JSON_REPO, TEMP_REPO_DIR
    ], check=True)

    src_header = os.path.join(TEMP_REPO_DIR, "single_include", "nlohmann", "json.hpp")
    if not os.path.exists(src_header):
        raise FileNotFoundError(f"json.hpp not found in cloned repo at {src_header}")

    shutil.move(src_header, JSON_HEADER)
    print(f"json.hpp installed to {JSON_HEADER}")

    shutil.rmtree(TEMP_REPO_DIR)
    print("Temporary clone folder removed.")

def run_cmake(samples=False, arm=False, tests=False):
    """Configure and build the project via CMake."""
    if tests:
        build_dir = BUILD_DIR_TESTS
    else:
        build_dir = BUILD_DIR_ARM if arm else BUILD_DIR_X86

    # Always create a fresh folder for ARM/x86/test builds
    if os.path.exists(build_dir):
        print(f"Removing existing build folder: {build_dir}")
        shutil.rmtree(build_dir)
    os.makedirs(build_dir, exist_ok=True)

    cmake_args = ["cmake", PROJECT_ROOT]
    cmake_args.append(f"-DBUILD_WITH_SAMPLES={'ON' if samples else 'OFF'}")
    cmake_args.append(f"-DBUILD_TESTS={'ON' if tests else 'OFF'}")
    cmake_args.append(f"-DBUILD_FOR_ARM={'ON' if arm else 'OFF'}")

    if arm:
        if not os.path.exists(TOOLCHAIN_FILE):
            print(f"Error: Toolchain file not found at {TOOLCHAIN_FILE}")
            sys.exit(1)
        cmake_args.append(f"-DCMAKE_TOOLCHAIN_FILE={TOOLCHAIN_FILE}")

    # Set RUNTIME_OUTPUT_DIRECTORY inside the build folder
    cmake_args.append(f"-DCMAKE_RUNTIME_OUTPUT_DIRECTORY={build_dir}/bin")

    print(f"Configuring project in {build_dir} with: {' '.join(cmake_args)}")
    subprocess.run(cmake_args, cwd=build_dir, check=True)

    print(f"Building project in {build_dir}...")
    subprocess.run(["cmake", "--build", "."], cwd=build_dir, check=True)
    print(f"Build complete! Binaries are in {build_dir}/bin")

def parse_args():
    """Parse command-line flags."""
    samples = False
    do_setup = False
    do_build = False
    build_for_arm = False
    build_tests = False

    for arg in sys.argv[1:]:
        if arg in ("--setup", "-s"):
            do_setup = True
        elif arg in ("--build", "-b"):
            do_build = True
        elif arg in ("--build-samples", "-S"):
            do_build = True
            samples = True
        elif arg in ("--arm", "-a"):
            do_build = True
            build_for_arm = True
        elif arg in ("--tests", "-t"):
            do_build = True
            build_tests = True
        else:
            print(f"Unknown argument: {arg}")
            sys.exit(1)

    return do_setup, do_build, samples, build_for_arm, build_tests

# ----------- Main -----------

if __name__ == "__main__":
    setup_flag, build_flag, samples_flag, arm_flag, tests_flag = parse_args()

    if setup_flag:
        run_setup()
    if build_flag:
        run_cmake(samples_flag, arm_flag, tests_flag)
    if not (setup_flag or build_flag):
        print(
            "Usage: python3 build.py [--setup|-s] [--build|-b] "
            "[--build-samples|-S] [--arm|-a] [--tests|-t]"
        )
