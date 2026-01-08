#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

# Configuration
JSON_REPO = "https://github.com/nlohmann/json.git"
JSON_INCLUDE_DIR = "include/nlohmann"
JSON_HEADER = os.path.join(JSON_INCLUDE_DIR, "json.hpp")
TEMP_REPO_DIR = "tmp_json_repo"
BUILD_DIR = "build"

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

    src_header = os.path.join(TEMP_REPO_DIR, "single_include/nlohmann/json.hpp")
    if not os.path.exists(src_header):
        raise FileNotFoundError(f"json.hpp not found in cloned repo at {src_header}")

    # Move header into include folder
    shutil.move(src_header, JSON_HEADER)
    print(f"json.hpp installed to {JSON_HEADER}")

    # Clean up temp folder
    shutil.rmtree(TEMP_REPO_DIR)
    print("Temporary clone folder removed.")

def run_cmake(samples=False):
    """Run CMake to configure and build project."""
    os.makedirs(BUILD_DIR, exist_ok=True)
    cmake_args = ["cmake", ".."]
    cmake_args.append(f"-DBUILD_WITH_SAMPLES={'ON' if samples else 'OFF'}")

    print(f"Configuring project with: {' '.join(cmake_args)}")
    subprocess.run(cmake_args, cwd=BUILD_DIR, check=True)

    print("Building project...")
    subprocess.run(["cmake", "--build", "."], cwd=BUILD_DIR, check=True)
    print("Build complete!")

def parse_args():
    """Parse command-line flags."""
    samples = False
    do_setup = False
    do_build = False

    for arg in sys.argv[1:]:
        if arg in ("--setup", "-s"):
            do_setup = True
        elif arg in ("--build", "-b"):
            do_build = True
        elif arg in ("--build-samples", "-S"):
            do_build = True
            samples = True
        else:
            print(f"Unknown argument: {arg}")
            sys.exit(1)
    return do_setup, do_build, samples

# ----------- Main -----------

if __name__ == "__main__":
    setup_flag, build_flag, samples_flag = parse_args()

    if setup_flag:
        run_setup()
    if build_flag:
        run_cmake(samples_flag)
    if not (setup_flag or build_flag):
        print("Usage: python3 build.py [--setup|-s] [--build|-b] [--build-samples|--samples]")
