#!/usr/bin/env python3
import os
import subprocess

REPO_URL = "https://github.com/nlohmann/json.git"
INCLUDE_DIR = "include/nlohmann"

# Ensure include folder exists
os.makedirs(INCLUDE_DIR, exist_ok=True)

# Clone only if json.hpp does not already exist
json_header = os.path.join(INCLUDE_DIR, "json.hpp")
if not os.path.exists(json_header):
    print(f"Cloning nlohmann/json into {INCLUDE_DIR}...")
    subprocess.run([
        "git", "clone", "--depth", "1",
        REPO_URL,
        "tmp_json_repo"
    ], check=True)

    # Copy single include file
    os.rename("tmp_json_repo/single_include/nlohmann/json.hpp", json_header)

    # Remove the temporary repo folder
    subprocess.run(["rm", "-rf", "tmp_json_repo"])
    print("Done! json.hpp is ready to use.")
else:
    print("json.hpp already exists, skipping download.")
