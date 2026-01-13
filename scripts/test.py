#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path

BUILD_DIR = Path("build-tests")

def run(cmd):
    print(f"$ {' '.join(cmd)}")
    subprocess.check_call(cmd)

def main():
    try:
        run([
            "cmake",
            "-S", ".",
            "-B", str(BUILD_DIR),
            "-DBUILD_TESTS=ON",
        ])

        run([
            "cmake",
            "--build", str(BUILD_DIR),
        ])

        run([
            "ctest",
            "--test-dir", str(BUILD_DIR),
            "--output-on-failure",
        ])

        print("\nAll tests passed ✅")
        return 0

    except subprocess.CalledProcessError as e:
        print("\nTests failed ❌")
        return e.returncode

if __name__ == "__main__":
    sys.exit(main())
